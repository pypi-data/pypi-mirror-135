from typing import Callable

import torch
from torch import nn

from src.bayne.bounds.util import notnull, add_method


def linear_bound_propagation(model):
    @torch.no_grad()
    def crown_ibp(self: nn.Sequential, lower, upper):
        with notnull(getattr(model, '_pyro_context', None)):
            batch_size = lower.size(0)

            alpha, beta = compute_alpha_beta(model, lower, upper)
            linear_bounds = compute_linear_bounds(model, alpha, beta, batch_size)

            return linear_bounds

    add_method(model, 'crown_ibp', crown_ibp)

    return model


@torch.no_grad()
def interval_bounds(self, model, lower, upper):
    (Omega_0, Omega_accumulator), (Gamma_0, Gamma_accumulator) = self.linear_bounds(model, lower, upper)

    # lower, upper = lower.unsqueeze(-2), upper.unsqueeze(-2)

    # We can do this instead of finding the Q-norm, as we only deal with perturbation over a hyperrectangular input,
    # and not a B_p(epsilon) ball
    mid = (lower + upper) / 2
    diff = (upper - lower) / 2

    min_Omega_x = mid * Omega_0 - diff * torch.abs(Omega_0)
    max_Gamma_x = mid * Gamma_0 + diff * torch.abs(Gamma_0)

    return min_Omega_x + Omega_accumulator, max_Gamma_x + Gamma_accumulator


def compute_alpha_beta(model, lower, upper):
    LBs, UBs = model.ibp(lower, upper, pre=True)

    alpha, beta = [], []

    for module, LB, UB in zip(model, LBs, UBs):
        n = UB <= 0
        p = LB >= 0
        np = (LB < 0) & (0 < UB)

        if isinstance(module, nn.ReLU):
            a, b = compute_alpha_beta_relu(LB, UB, n, p, np)
        elif isinstance(module, nn.Sigmoid):
            a, b = compute_alpha_beta_sigmoid(LB, UB, n, p, np)
        elif isinstance(module, nn.Tanh):
            a, b = compute_alpha_beta_tanh(LB, UB, n, p, np)
        else:
            a, b = (None, None), (None, None)

        alpha.append(a)
        beta.append(b)

    return alpha, beta


def compute_alpha_beta_relu(LB, UB, n, p, np, adaptive_relu=True):
    alpha_lower_k = torch.zeros_like(LB)
    alpha_upper_k = torch.zeros_like(LB)
    beta_lower_k = torch.zeros_like(LB)
    beta_upper_k = torch.zeros_like(LB)

    alpha_lower_k[n] = 0
    alpha_upper_k[n] = 0
    beta_lower_k[n] = 0
    beta_upper_k[n] = 0

    alpha_lower_k[p] = 1
    alpha_upper_k[p] = 1
    beta_lower_k[p] = 0
    beta_upper_k[p] = 0

    LB, UB = LB[np], UB[np]

    z = UB / (UB - LB)
    if adaptive_relu:
        a = (UB >= torch.abs(LB)).to(torch.float)
    else:
        a = z

    alpha_lower_k[np] = a
    alpha_upper_k[np] = z
    beta_lower_k[np] = 0
    beta_upper_k[np] = -LB * z

    return (alpha_lower_k, alpha_upper_k), (beta_lower_k, beta_upper_k)


def compute_alpha_beta_sigmoid(LB, UB, n, p, np):
    return compute_alpha_beta_general(LB, UB, n, p, np, torch.sigmoid)


def compute_alpha_beta_tanh(LB, UB, n, p, np):
    return compute_alpha_beta_general(LB, UB, n, p, np, torch.tanh)


def compute_alpha_beta_general(LB, UB, n, p, np, func):
    @torch.enable_grad()
    def derivative(d):
        d.requires_grad_()
        y = func(d)
        y.backward(torch.ones_like(d))

        return d.grad

    alpha_lower_k = torch.zeros_like(LB)
    alpha_upper_k = torch.zeros_like(LB)
    beta_lower_k = torch.zeros_like(LB)
    beta_upper_k = torch.zeros_like(LB)

    LB_act, UB_act = func(LB), func(UB)

    d = (LB + UB) * 0.5  # Let d be the midpoint of the two bounds
    d_act = func(d)
    d_prime = derivative(d)

    concave_slope = torch.nan_to_num((UB_act - LB_act) / (UB - LB), nan=0.0)

    # Negative regime
    alpha_lower_k[n] = d_prime[n]
    alpha_upper_k[n] = concave_slope[n]
    beta_lower_k[n] = d_act[n] - alpha_lower_k[n] * d[n]
    beta_upper_k[n] = UB_act[n] - alpha_upper_k[n] * UB[n]

    # Positive regime
    alpha_lower_k[p] = concave_slope[p]
    alpha_upper_k[p] = d_prime[p]
    beta_lower_k[p] = LB_act[p] - alpha_lower_k[p] * LB[p]
    beta_upper_k[p] = d_act[p] - alpha_upper_k[p] * d[p]

    # Crossing zero
    LB_np, UB_np = LB[np], UB[np]

    def f_lower(d):
        return derivative(d) - (func(UB_np) - func(d)) / (UB_np - d)

    def f_upper(d):
        return (func(d) - func(LB_np)) / (d - LB_np) - derivative(d)

    d_lower = bisection(LB_np, torch.zeros_like(LB_np), f_lower)
    d_upper = bisection(torch.zeros_like(UB_np), UB_np, f_upper)

    alpha_lower_k[np] = derivative(d_lower)
    alpha_upper_k[np] = derivative(d_upper)
    beta_lower_k[np] = UB_act[np] - alpha_lower_k[np] * UB_np
    beta_upper_k[np] = LB_act[np] - alpha_upper_k[np] * LB_np

    return (alpha_lower_k, alpha_upper_k), (beta_lower_k, beta_upper_k)


def bisection(l: torch.Tensor, h: torch.Tensor, f: Callable[[torch.Tensor], torch.Tensor], num_iter=10) -> torch.Tensor:
    midpoint = (l + h) / 2
    y = f(midpoint)

    for _ in range(num_iter):
        l[y <= 0] = midpoint[y <= 0]
        h[y > 0] = midpoint[y > 0]

        midpoint = (l + h) / 2
        y = f(midpoint)

    return midpoint


def compute_linear_bounds(model, alpha, beta, batch_size):
    output_size = model[-1].weight.size(-2)

    Omega_tilde = torch.eye(output_size).unsqueeze(0).expand(batch_size, output_size, output_size)
    Gamma_tilde = torch.eye(output_size).unsqueeze(0).expand(batch_size, output_size, output_size)

    Omega_acc = 0
    Gamma_acc = 0

    # List is necessary around zip to allow reversing
    for module, (al_k, au_k), (bl_k, bu_k) in reversed(list(zip(model, alpha, beta))):
        with notnull(getattr(module, '_pyro_context', None)):
            if isinstance(module, nn.Linear):
                Omega_tilde, omega = linear(Omega_tilde, module)
                Omega_acc = Omega_acc + omega

                Gamma_tilde, gamma = linear(Gamma_tilde, module)
                Gamma_acc = Gamma_acc + gamma
            elif isinstance(module, (nn.ReLU, nn.Tanh, nn.Sigmoid)):
                Omega_tilde, omega = act_lower(Omega_tilde, al_k, au_k, bl_k, bu_k)
                Omega_acc = Omega_acc + omega

                Gamma_tilde, gamma = act_upper(Gamma_tilde, al_k, au_k, bl_k, bu_k)
                Gamma_acc = Gamma_acc + gamma
            else:
                raise NotImplemented()

    return (Omega_tilde, Omega_acc), (Gamma_tilde, Gamma_acc)


def linear(W_tilde, module):
    bias = module.bias
    weight = module.weight

    if weight.dim() == 2:
        W_tilde_new = torch.matmul(W_tilde, weight)
    else:
        if W_tilde.dim() == 3:
            W_tilde = W_tilde.unsqueeze(0)

        W_tilde_new = torch.matmul(W_tilde, weight.unsqueeze(1))

    if bias is None:
        bias_acc = 0
    elif bias.dim() == 1:
        bias_acc = torch.matmul(W_tilde, bias)
    else:
        bias = bias.view(bias.size(0), 1, bias.size(-1), 1)
        bias_acc = torch.matmul(W_tilde, bias)[..., 0]

    return W_tilde_new, bias_acc


def act_lower(Omega_tilde, al_k, au_k, bl_k, bu_k):
    bias = torch.sum(Omega_tilde * _theta(Omega_tilde, bl_k, bu_k), dim=-1)
    Omega_tilde = Omega_tilde * _omega(Omega_tilde, al_k, au_k)

    return Omega_tilde, bias


def _theta(omega_weight, beta_lower, beta_upper):
    return torch.where(omega_weight < 0, beta_upper.unsqueeze(-2), beta_lower.unsqueeze(-2))


def _omega(omega_weight, alpha_lower, alpha_upper):
    return torch.where(omega_weight < 0, alpha_upper.unsqueeze(-2), alpha_lower.unsqueeze(-2))


def act_upper(Gamma_tilde, al_k, au_k, bl_k, bu_k):
    bias = torch.sum(Gamma_tilde * _delta(Gamma_tilde, bl_k, bu_k), dim=-1)
    Gamma_tilde = Gamma_tilde * _lambda(Gamma_tilde, al_k, au_k)

    return Gamma_tilde, bias


def _delta(gamma_weight, beta_lower, beta_upper):
    return torch.where(gamma_weight < 0, beta_lower.unsqueeze(-2), beta_upper.unsqueeze(-2))


def _lambda(gamma_weight, alpha_lower, alpha_upper):
    return torch.where(gamma_weight < 0, alpha_lower.unsqueeze(-2), alpha_upper.unsqueeze(-2))
