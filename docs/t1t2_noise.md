# Probabililities for the Pauli channels

The probabilities for the Pauli channels have been obtained from: [arXiv:1210.5799v2](https://arxiv.org/pdf/1210.5799.pdf). 

The summary of the procedure is:
- Obtain the Kraus operators $\\{E_i\\}$ for the amplitude damping (AD) channel and the phase damping (PD) channel
```math
\Lambda_{AD}(\rho) = \sum_i E_{AD,i} \rho E_{AD,i}^{\dagger} \quad \Lambda_{PD}(\rho) = \sum_i E_{PD,i} \rho E_{PD,i}^{\dagger}
```

- The Kraus operators for the combination of these channels are the combinations of these oeprators
```math
\Lambda(\rho) = \Lambda_{AD}(\Lambda_{PD}(\rho)) = \Lambda_{PD}(\Lambda_{AD}(\rho)) = \sum_{i,j} E_{AD,i} E_{PD,i} \rho E_{AD,i}^{\dagger} E_{PD,i}^{\dagger} \equiv \sum_k E_k \rho E_k
```
*Note: one of the resulting Kraus operator is* $E_k = 0$ *thus it is ommited and we only work with 3 operators.*

- Express $E_k$ in terms of the Pauli matrices, i.e. $E_k = \sum_i a_i^{(k)} \sigma_i$. 

- Rewrite $\Lambda(\rho)$ in terms of Pauli matrices

- Apply Pauli Twirl Approximation (PTA), which consists of removing the cross terms, e.g. $X\rho Y$. 

- Extract $p_X, p_Y, p_Z$ from 
```math
\Lambda_{PTA}(\rho) \equiv (1 - p_X - p_Y - p_Z)\rho + p_X X\rho X + p_Y Y\rho Y + p_Z Z\rho Z
```
*Note: these probabilities depend on the parameters of* $E_{AD,i}$ *and* $E_{PD,i}$ *which depend on the duration of the noise channel and the T1 and T2 times*.

The final result is:
```math
p_X = p_Y = \frac{1 - e^{-t/T_1}}{4} \quad p_Z = \frac{1 - e^{-t/T_2}}{2} - \frac{1 - e^{-t/T_1}}{4}
```
