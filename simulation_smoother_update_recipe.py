import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

N = 12
L = 10.0
dt = 0.01
T = 500

rd = 0.5 #diameter of the molecule
radius = rd/2

pos = np.random.rand(N, 2)*L
vel = (np.random.rand(N, 2) - 0.5) * 25
mass = np.ones(N)


# FUNCTION GIVEN IN THE PDF.
# def walls_reflect ( pos , vel , L ):
#     # Left wall (x < 0)
#     left_hits = pos [: , 0] < 0
#     vel [ left_hits , 0] *= -1 # flip x velocity
#     pos [ left_hits , 0] = 0.0 # push back inside

#     # Right wall (x > L)
#     right_hits = pos [: , 0] > L
#     vel [ right_hits , 0] *= -1
#     pos [ right_hits , 0] = L

#     # Bottom wall (y < 0)
#     bottom_hits = pos [: , 1] < 0
#     vel [ bottom_hits , 1] *= -1
#     pos [ bottom_hits , 1] = 0.0

#     # Top wall (y > L)
#     top_hits = pos [: , 1] > L
#     vel [ top_hits , 1] *= -1
#     pos [ top_hits , 1] = L

#     return pos , vel



# MODIFIED AND REFINED FUNCTION
def walls_reflect(pos, vel, L):
    for i in range(N):
        if pos[i,0] - radius <0:
            vel[i,0] *= -1
            pos[i,0] = radius

        if pos[i,0] + radius > L:
            vel[i, 0] *= -1
            pos[i, 0] = L - radius
        if pos[i, 1] - radius < 0:
            vel[i, 1] *= -1
            pos[i, 1] = radius
        if pos[i, 1] + radius > L:
            vel[i, 1] *= -1
            pos[i, 1] = L - radius
    return pos, vel

def distance(x1,y1,x2,y2):
    dis = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dis

#where k is stiffness, r0 is preferred spacing and rc is the cutoff distance.
k = 30.0
r0 = 1.5
rc = 2.0 # cutoff distance

def pair_forces(pos):
    F = np.zeros_like(pos)
    for i in range (len(pos)):
        for j in range (i+1, len(pos)):
            r_vec = pos[i] - pos[j]
            r = distance(pos[i,0],pos[i,1],pos[j,0],pos[j,1])
            if r<rc and r>1e-12:
                f_mag = -k * (r-r0)
                f_vec = f_mag * (r_vec/r)
                F[i] += f_vec
                F[j] -= f_vec
    
    return F

F = pair_forces(pos)

def step_smooth ( pos , vel , mass , dt , L , F_prev = None ):
        
        # 1. Force at old positions
        if F_prev is None :
            F_prev = pair_forces( pos )
            a_prev = F_prev / mass [: , None ]

        # 2. Half velocity update
        vel_half = vel + 0.5 * a_prev * dt

        # 3. Move positions
        pos_new = pos + vel_half * dt

        pos_new, vel_half = walls_reflect ( pos_new , vel_half , L )

        # 4. New forces
        F_new = pair_forces ( pos_new )
        a_new = F_new / mass [: , None ]

        # 5. Finish velocity update
        vel_new = vel_half + 0.5 * a_new * dt
        return pos_new , vel_new , F_new


def kinetic_energy(vel, mass):
    KE=[]
    for v in range(len(vel)):
        E = 0.5*(mass)*(vel[v,0]**2 + vel[v,1]**2)
        KE.append(E)
    KE_total = np.sum(KE)
    return KE_total


#TODO after step_smooth 
# The Kinetic energy fluctuations are less than earlier .
# When the value of dt is increased the fluctuations are very huge.

plt.ion()
fig, ax = plt.subplots()
ax.set_xlim(0, L)
ax.set_ylim(0, L)
scat = ax.scatter(pos[:, 0], pos[:, 1], s=100)

KE_total_new = []
step = 0

while step < T:
    pos, vel, F= step_smooth(pos, vel, mass, dt, L, F_prev=None)
    KE_total_new.append(kinetic_energy(vel, mass))

    scat.set_offsets(pos)

    ax.set_title(f"Step {step} | KE={KE_total_new[-1]:.2f}")

    plt.pause(0.02)
    step+=1

plt.ioff()


plt.figure()
plt.plot(range(1, len(KE_total_new)+1), KE_total_new)
plt.ylim(0, max(KE_total_new))
plt.xlabel("Step")
plt.ylabel("Total Kinetic Energy")
plt.title("KE vs Simulation Step")
plt.grid(True)
plt.show()










    