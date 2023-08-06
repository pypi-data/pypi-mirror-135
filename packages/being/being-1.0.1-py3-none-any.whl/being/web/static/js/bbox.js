/**
 * Bounding box. Progressively expand a 2D region.
 *
 * @module js/bbox
 */
import { clip } from "/static/js/math.js";


/**
 * Two dimensional bounding box.
 *
 * @param {array} [ll=[Infinity, Infinity] - Lower left point.
 * @param {array} [ur=[-Infinity, -Infinity] - Upper right point.
 *
 * @example
 * bbox = new BBox();
 * bbox.expand_by_point([1, 1]);
 * bbox.expand_by_point([3, 2]);
 * // outputs [2, 1]
 * console.log(bbox.size);
 */
export class BBox {
    constructor(ll=[Infinity, Infinity], ur=[-Infinity, -Infinity]) {
        this.ll = ll;
        this.ur = ur;
    }

    /**
     * Bounding box size.
     * @type {array}
     */
    get size() {
        return [
            this.ur[0] - this.ll[0],
            this.ur[1] - this.ll[1],
        ];
    }

    /**
     * Bounding box width.
     * @type {number}
     */
    get width() {
        return this.ur[0] - this.ll[0];
    }

    /**
     * Bounding box height.
     * @type {number}
     */
    get height() {
        return this.ur[1] - this.ll[1];
    }

    /**
     * Get / set leftmost x value.
     * @type {number}
     */
    get left() {
        return this.ll[0];
    }

    set left(pos) {
        this.ll[0] = pos;
    }

    /**
     * Get / set rightmost x value.
     * @type {number}
     */
    get right() {
        return this.ur[0];
    }

    set right(value) {
        this.ur[0] = value;
    }

    /**
     * Reset to infinite bounding box.
     */
    reset() {
        this.ll = [Infinity, Infinity];
        this.ur = [-Infinity, -Infinity];
    }

    /**
     * Expand bounding box region.
     *
     * @param {array} pt - Point to add to bounding box.
     */
    expand_by_point(pt) {
        this.ll[0] = Math.min(this.ll[0], pt[0]);
        this.ll[1] = Math.min(this.ll[1], pt[1]);
        this.ur[0] = Math.max(this.ur[0], pt[0]);
        this.ur[1] = Math.max(this.ur[1], pt[1]);
    }

    /**
     * Expand bounding box region for some point.
     *
     * @param {array} pts - Points to add to bounding box.
     */
    expand_by_points(pts) {
        pts.forEach(pt => this.expand_by_point(pt));
    }

    /**
     * Expand bounding box region for another bounding box.
     *
     * @param {BBox} bbox - Bounding box to expand this bounding box with.
     */
    expand_by_bbox(bbox) {
        this.expand_by_point(bbox.ll);
        this.expand_by_point(bbox.ur);
    }

    /**
     * Clip point inside bounding box.
     *
     * @param {Array} pt - 2D point to clip.
     *
     * @returns {Array} Clipped point.
     */
    clip_point(pt) {
        return [
            clip(pt[0], this.ll[0], this.ur[0]),
            clip(pt[1], this.ll[1], this.ur[1]),
        ];
    }

    /**
     * Copy bounding box.
     *
     * @returns {BBox} New bounding box copy.
     */
    copy() {
        return new BBox([...this.ll], [...this.ur]);
    }

    /**
     * Check if bounding box is finite.
     *
     * @returns {boolean} If finite.
     */
    is_finite() {
        const numbers = [this.ll, this.ur].flat();
        return numbers.every(Number.isFinite);
    }
}
