import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def resample_trajectory(points, num_points):
    """
    Resample a trajectory (Nx3) to have exactly `num_points` samples using arc-length interpolation.
    """
    points = np.array(points)
    dists = np.linalg.norm(np.diff(points, axis=0), axis=1)
    arc_lengths = np.concatenate([[0], np.cumsum(dists)])
    total_length = arc_lengths[-1]

    # Normalize arc-length to [0, 1]
    arc_lengths /= total_length
    target_lengths = np.linspace(0, 1, num_points)

    # Interpolate each axis
    interp = [interp1d(arc_lengths, points[:, dim], kind='linear') for dim in range(3)]
    resampled = np.stack([f(target_lengths) for f in interp], axis=-1)
    return resampled

def procrustes_align(A, B):
    """
    Aligns trajectory B to A using Procrustes analysis. Returns aligned B and RMSE.
    """
    A_mean = np.mean(A, axis=0)
    B_mean = np.mean(B, axis=0)
    A_centered = A - A_mean
    B_centered = B - B_mean

    H = B_centered.T @ A_centered
    U, _, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = Vt.T @ U.T

    B_aligned = B_centered @ R
    rmse = np.sqrt(np.mean(np.linalg.norm(A_centered - B_aligned, axis=1)**2))
    return B_aligned + A_mean, rmse

def generate_sample_trajectories():
    """
    Generate two sample 3D trajectories of different lengths.
    """
    t1 = np.linspace(0, 2 * np.pi, 100)
    A = np.stack([np.cos(t1), np.sin(t1), t1 / np.pi], axis=1)

    t2 = np.linspace(0, 2 * np.pi, 70)  # shorter version
    B = np.stack([np.cos(t2), np.sin(t2), t2 / np.pi], axis=1)

    # Rotate and translate B
    theta = np.pi / 4
    R = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0,              0,             1]
    ])
    B = (B @ R.T) + np.array([0.5, -1.0, 0.2])
    return A, B

def plot_trajectories(A, B_raw, B_aligned):
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(*A.T, label='A', color='blue')
    ax1.plot(*B_raw.T, label='B (original)', color='red')
    ax1.set_title("Before Alignment")
    ax1.legend()

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot(*A.T, label='A', color='blue')
    ax2.plot(*B_aligned.T, label='B (aligned)', color='green')
    ax2.set_title("After Procrustes Alignment")
    ax2.legend()

    plt.tight_layout()
    plt.show()

def main():
    A, B = generate_sample_trajectories()

    # Resample to equal size
    N = 100
    A_resampled = resample_trajectory(A, N)
    B_resampled = resample_trajectory(B, N)

    # Align and compare
    B_aligned, rmse = procrustes_align(A_resampled, B_resampled)
    print(f"RMSE after alignment: {rmse:.6f}")

    # Plot results
    plot_trajectories(A_resampled, B_resampled, B_aligned)

if __name__ == "__main__":
    main()
