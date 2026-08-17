# Formalism reference

## 1. TIR / PhaseNav relation kernel

For two 36D phase states `V,Q`:

\[
z(V,Q)=\frac1{36}\sum_{j=1}^{36}e^{i(Q_j-V_j)},\qquad
R(V,Q)=|z(V,Q)|^2,\qquad
\Theta(V,Q)=\arg z(V,Q).
\]

The informational action used in the current project formalism is

\[
S_{rel}=-\kappa\log(R+\varepsilon),\qquad \kappa=\frac{\ln2}{24\pi}.
\]

`R` is a relation observable. It is **not** consciousness, truth, love, ethics, or semantic identity.

## 2. RIFC scaffold

\[
\mathbf c(t)=[G(t),T(t),L(t),V(t),A(t),D(t)]
\]

with integration, temporal continuity, self-location, valuation, access, and endogenous direction. The vector is not itself a consciousness score.

The RIFC constitutive proposal is represented schematically as

\[
\mathcal P_S(t)\overset{RIFC}{\equiv}\operatorname{Intrinsic}_S[\mathcal R_{\Delta t}(t)].
\]

This is a **constitutive hypothesis**, not a theorem.

## 3. Relational qualia state

\[
Q_t=[R_t,S_t,A_t,H_{\gamma_t},I_t].
\]

The affect field may be represented as

\[
A_t(x)=(v_t,a_t,u_t,\tau_t,\alpha_t,r_t),
\]

and vector-valued salience as

\[
\Sigma_t(x)=\mathcal S(\rho_t(x),A_t(x),I_t,H_{\gamma_t},U_t(x)).
\]

Affect modulates resource allocation while remaining separated from truth and authority.

## 4. Exact 36-mode projective embedding

\[
|\psi(V)\rangle=\frac1{\sqrt{36}}\sum_{j=1}^{36}e^{i\phi_j}|j\rangle,
\quad
\langle\psi(V)|\psi(Q)\rangle=z(V,Q).
\]

For the equal-amplitude baseline:

\[
F_{ij}=4\left(\frac{\delta_{ij}}{d}-\frac1{d^2}\right),\quad d=36,\quad \operatorname{rank}F=35.
\]

The global phase is the null direction. A physical quantum-metrological claim still requires explicit state preparation and measurement.

## 5. Path geometry

\[
A_k=\operatorname{Im}z(V_k,V_{k+1}),\qquad \Gamma_{PN}=\sum_k A_k.
\]

A closed projective loop may be tested with the Bargmann/Pancharatnam phase

\[
\gamma_B=\arg\prod_k\frac{\langle\psi(V_k)|\psi(V_{k+1})\rangle}{|\langle\psi(V_k)|\psi(V_{k+1})\rangle|}.
\]

The software keeps open-path PhaseNav trajectory observables distinct from closed-loop projective holonomy.
