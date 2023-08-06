/**
 * Numpy style array helpers. Most of these functions operate on standard and
 * nested JS arrays (like [0, 1, 2, 3] or [[0, 1, 2], [3, 4, 5]]).
 *
 * @module js/array
 *
 * @todo The whole thing could probabelly be replaced by the math.js library... 
 */
import {assert, arrays_equal} from "/static/js/utils.js";


/**
 * Determine array shape.
 *
 * @param {array} arr - Input array.
 *
 * @returns {array} array shape.
 */
export function array_shape(arr) {
    let shape = [];
    while (arr instanceof Array) {
        shape.push(arr.length);
        arr = arr[0];
    }

    return shape;
}


/**
 * Number of array dimensions.
 *
 * @param {array} arr - Input array.
 *
 * @returns Number of array
 */
export function array_ndims(arr) {
    return array_shape(arr).length;
}


/**
 * Reshape an array. (Taken from _reshape function from the math.js library).
 *
 * @param {array} arr - Input array.
 * @param {array} shape - New array shape.
 *
 * @returns Reshaped array.
 */
export function array_reshape(arr, shape) {
    let tmpArray = arr;
    let tmpArray2;
    for (let sizeIndex = shape.length - 1; sizeIndex > 0; sizeIndex--) {
        const size = shape[sizeIndex];
        tmpArray2 = [];
        const length = tmpArray.length / size;
        for (let i = 0; i < length; i++) {
            tmpArray2.push(tmpArray.slice(i * size, (i + 1) * size));
        }
        tmpArray = tmpArray2;
    }

    return tmpArray;
}


/**
 * Minimum value in array.
 *
 * @param {array} arr - Input array.
 *
 * @returns Minimum value.
 */
export function array_min(arr) {
    return Math.min.apply(Math, arr.flat());
}


/**
 * Maximum value in array.
 *
 * @param {array} arr - Input array.
 *
 * @returns Maximum value.
 */
export function array_max(arr) {
    return Math.max.apply(Math, arr.flat());
}


/**
 * Create a new array filled with zeros.
 *
 * @param {array} shape - Input shape
 *
 * @returns {array} Zero array of given shape
 */
export function zeros(shape) {
    let array = [];
    for (let i = 0; i < shape[0]; i++) {
        array.push(shape.length === 1 ? 0 : zeros(shape.slice(1)));
    }

    return array;
}


/**
 * Ascending integer array.
 *
 * @param {number} start - Start index.
 * @param {number|undefined} [stop=undefined] - Stop index (not included).
 * @param {number} [step=1] - Step size.
 *
 * @returns Range array.
 *
 * @example
 * // returns [0, 1, 2, 3, 4]
 * arange(5)
 *
 * @example
 * // returns [2, 3, 4]
 * arange(2, 5)
 *
 * @example
 * // returns [0, 2, 4]
 * arange(0, 5, 2)
 */
export function arange(start, stop=undefined, step=1) {
    if (stop === undefined) {
        [start, stop] = [0, start];
    }

    const ret = [];
    for (let i=start; i<stop; i+=step) {
        ret.push(i);
    }

    return ret;
}


/**
 * Ascending linspace array.
 *
 * @param {number} [start=0.0] - Start value.
 * @param {number} [stop=1.0] - End value.
 * @param {number} [num=50] - Number of entries.
 *
 * @returns {array} Linspace array.
 */
export function linspace(start=0.0, stop=1.0, num=50) {
    console.assert(num > 1, "num > 1!");
    const step = (stop - start) / (num - 1);
    return arange(num).map((i) => i * step);
}

/**
 * Element wise add two arrays together.
 *
 * @param {array} augend - First operand.
 * @param {array} addend - Second operand.
 *
 * @returns {array} Added array.
 *
 * @example
 * // returns [3, 6]
 * add_arrays([1, 2], [2, 4]);
 */
export function add_arrays(augend, addend) {
    return augend.map((aug, i) => aug + addend[i]);
}


/**
 * Multiply scalar factor with array.
 *
 * @param {number} factor - Scalar factor.
 * @param {array} arr - Array to multiply.
 *
 * @returns {array} Multiplied array.
 *
 * @example
 * // returns [3, 6, 9]
 * multiply_scalar(3, [1, 2, 3]);
 */
export function multiply_scalar(factor, arr) {
    return arr.map(e => factor * e);
}


/**
 * Element wise divide two arrays.
 *
 * @param {array} dividend - Left operand.
 * @param {array} divisor - Right operand.
 *
 * @returns {array} Divided array.
 */
export function divide_arrays(dividend, divisor) {
    return dividend.map((div, i) => div / divisor[i]);
}


/**
 * Element wise subtract two array from each other.
 *
 * @param {array} minuend - Left operand.
 * @param {array} subtrahend - Right operand.
 *
 * @returns {array} Difference array.
 */
export function subtract_arrays(minuend, subtrahend) {
    return minuend.map((min, i) => min - subtrahend[i]);
}


/**
 * Transpose array. Works only for 2d arrays.
 *
 * @param {array} arr - Array to transpose.
 *
 * @returns {array} Transposed array.
 *
 * @example
 * // returns [[1, 2, 3]]
 * transpose_array([[1], [2], [3]])
 */
export function transpose_array(arr) {
    return arr[0].map((_, colIndex) => arr.map(row => row[colIndex]));
}


assert(arrays_equal( transpose_array([[1], [2], [3]]), [[1, 2, 3]] ));


/**
 * Return a new array of given shape filled with `fillValue`.
 *
 * @param {array} shape - Desired shape.
 * @param {number} fillValue - Fill value.
 *
 * @returns {array} Output array.
 */
export function array_full(shape, fillValue) {
    const n = shape.reduce((acc, val) => {
        return acc * val;
    });
    const raw = Array(n).fill(fillValue);
    return array_reshape(raw, shape);
}


assert(arrays_equal( array_full([3], 1), [1, 1, 1] ));
assert(arrays_equal( array_full([1, 3], 1), [[1, 1, 1]] ));


/**
 * Discrete difference along first axis. Only for 1D arrays.
 *
 * @param {array} arr - Input array.
 *
 * @returns {array} Difference. One shorter than input array!
 *
 * @example
 * // returns [1, 1]
 * diff_array([1, 2, 3])
 */
export function diff_array(arr) {
    const delta = [];
    for (let i=1; i<arr.length; i++) {
        delta.push(arr[i] - arr[i - 1]);
    }

    return delta;
}
