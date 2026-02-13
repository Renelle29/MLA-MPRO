using Random

function generate_manhattan(n::Int, m::Int; L::Int = 100, cost_range = 10:50, seed::Int = 1)
    
    Random.seed!(seed)

    total_points = (L + 1)^2
    @assert n + m <= total_points "Grid too small"

    grid = [(x, y) for x in 0:L, y in 0:L]

    selected = randperm(total_points)[1:(n+m)]
    points = grid[selected]

    coordinates_n = reduce(vcat, [reshape(collect(points[i]), 1, 2) for i in 1:n])
    coordinates_m = reduce(vcat, [reshape(collect(points[i]), 1, 2) for i in (n+1):(n+m)])

    f = rand(cost_range, m)

    return coordinates_n, coordinates_m, f
end