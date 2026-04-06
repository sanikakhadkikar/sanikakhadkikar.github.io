---
title: "Eccentricities in Gravitational Wave Binaries"
summary: "Why does eccentricity matter in compact binary systems if orbits circularize before merger? A walkthrough of orbital dynamics and gravitational wave emission."
date: "2024-06-01"
math: true
image: "/uploads/eccentricity.gif"
---

<div style="text-align: center; margin: 2em 0;">
<p style="font-style: italic; font-weight: bold;">"The most exciting phrase to hear in science, the one that heralds new discoveries, is not 'Eureka' but 'That's funny...'"</p>
<p style="font-style: italic; margin-top: 0.5em;"> -  Isaac Asimov</p>
</div>

Recently, I have noticed increased discussion on the importance of eccentricity in the gravitational wave (GW) compact object coalescence literature. However, I lack intuition for why eccentricity is considered significant, for the following reasons:

1. The orbits circularize ($e \to 0$) as the compact binary approaches coalescence due to gravitational wave emission. So why include eccentricity at all stages?
2. The eccentricities of binary neutron star (BNS) systems formed through isolated binary evolution channels are expected to be small ($e < 0.3$). Dynamically formed binaries contribute only a small fraction of the total BNS population.
3. The orbital period does not depend on eccentricity. To explore this, I begin by revisiting the basics of orbital dynamics.

The Lagrangian for a two-body system in the center-of-mass frame is:

$$\mathcal{L} = \frac{1}{2}\mu\dot{r}^2 + \frac{1}{2}\mu r^2 \dot{\theta}^2 + \frac{Gm_1m_2}{r}$$

Here, $\mu = \frac{m_1 m_2}{m_1 + m_2}$ is the reduced mass. Since $\theta$ is a cyclic coordinate, we have:

$$\mu r^2 \dot{\theta} = \ell$$

And the radial equation of motion becomes:

$$\mu \ddot{r} = \frac{\ell^2}{\mu r^3} - \frac{Gm_1m_2}{r^2}$$

Using the substitution $u = \frac{1}{r}$, the solution is a conic:

$$r(\theta) = \frac{\ell^2}{\mu^2 GM (1 + e \cos\theta)}$$

Here $M = m_1 + m_2$ and $e$ is the orbital eccentricity. The orbital radius $r$ depends on $e$, but the period $T$ is independent of it for bound orbits. By Kepler's second law:

$$\frac{dA}{dt} = \frac{1}{2} r^2 \frac{d\theta}{dt} = \frac{\ell}{2\mu} = \text{constant}$$

Integrating over a full orbit:

$$A = \frac{\ell T}{2\mu}$$

And for an ellipse:

$$A = \pi a b = \pi a^2 \sqrt{1 - e^2}$$

From the conic solution:

$$a(1 - e^2) = \frac{\ell^2}{\mu^2 GM}$$

Combining these results:

$$T^2 = \frac{4\pi^2}{GM} a^3$$

This is Kepler's third law, which confirms that the period $T$ is independent of eccentricity.

My skepticism about the emphasis on eccentricity is rooted in these points. However, the inclusion of gravitational radiation may alter this picture. I will explore this further in future work.
