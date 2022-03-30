import numpy as np
import matplotlib.pyplot as plt


def generateBoundary(m, T):
    for index in range(1, len(m[0]) - 1):
        m[0][index] = T


def plotMap(U, i, tempx, tempy, dt, ax=None):
    # For 2D plots
    cp = ax.imshow(U, cmap=plt.get_cmap("hot"), interpolation="gaussian")

    # For 3D plots
    # cp = ax.plot_surface(tempx, tempy, U, cmap=plt.get_cmap("hot"))
    # ax.set_zlabel("T(x,y,t)")

    ax.set_title("Iteration: {0}, Time: {1}".format(i, dt * i))
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.tick_params(axis="both", which="major", labelsize=9)
    ax.tick_params(axis="both", which="minor", labelsize=9)
    plt.colorbar(cp, ax=ax, fraction=0.046, pad=0.2)


def num_scheme(curr, ref, y, x, dt, dx):
    topNode = curr[y + 1][x]
    bottomNode = curr[y - 1][x]
    leftNode = curr[y][x - 1]
    rightNode = curr[y][x + 1]
    centerNode = curr[y][x]

    newNode = centerNode + (
        topNode + leftNode + bottomNode + rightNode - 4 * centerNode
    ) * dt / pow(dx, 2)

    ref[y][x] = newNode


def qn1a():
    size = 10  # matrix size
    T = 1.0
    dt = 0.0025  # time step
    n = 400  # iterations
    iter_to_plot = [1, 4, 40, 51]
    row_subplot_num = 2
    col_subplot_num = 2

    dx = 1 / size
    grid = np.zeros((size + 1, size + 1))

    conv_criteria = (dx * dx) / 6

    tempx = np.arange(0, 1.1, 0.1)
    tempy = np.flip(np.arange(0, 1.1, 0.1))
    tempx, tempy = np.meshgrid(tempx, tempy)

    plotted_ptr = 0
    plot_finish = False

    if row_subplot_num * col_subplot_num != len(iter_to_plot):
        raise Exception("Invalid subplot layout, check row and col nums")

    fig, axes = plt.subplots(
        col_subplot_num,
        row_subplot_num,
        figsize=(8, 6),
        constrained_layout=True,
        # subplot_kw={
        #     "projection": "3d"
        # },  # Projection argument is only for 3D, turn off if plotting 2D
    )
    plt.rcParams["font.size"] = "9"
    generateBoundary(grid, T)
    gridRef = np.copy(grid)

    converged = False
    i = 0
    while not converged:
        i += 1
        if i > n:
            print("Failed to converge at criteria: {0} dp".format(conv_criteria))
            break
        prevGrid = np.copy(grid)

        for y in range(1, size):
            for x in range(1, size):
                num_scheme(grid, gridRef, y, x, dt, dx)

        grid = np.copy(gridRef)
        max_diffs = np.subtract(grid, prevGrid).max()
        print(
            "Iter difference: {0} - {1}\n{2}".format(
                i, i - 1, np.subtract(grid, prevGrid)
            )
        )
        converged = True if max_diffs < conv_criteria else False

        if not plot_finish:
            if i == iter_to_plot[plotted_ptr]:
                # print("Iteration: {0}\n{1}\n\n".format(i, grid))
                ax = axes.flatten()
                plotMap(grid, i, tempx, tempy, dt, ax[plotted_ptr])
                plotted_ptr += 1
            if plotted_ptr == len(iter_to_plot):
                plot_finish = True

    print("\nConverged at {0}".format(i))
    plt.show()
