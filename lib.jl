module MyModule
using PyCall

function julia_function(arr::T)::eltype(T) where {T <: Matrix}
    s::eltype(T) = 0
    H = size(arr, 2)
    @inbounds for δ in 1:size(arr, 1)
        for j in 1:H
            @simd for i in 1:size(arr, 1)
                k = max(1, i - δ)
                h = min(H, j + δ)
                s += arr[i, j] + arr[k, h]
            end
        end
    end
    return s
end

# for PyObject/PyArray
function function_running_in_parallel(arr::T) where T
    return function_running_in_parallel(convert(Matrix{Float64}, arr))
end
end
