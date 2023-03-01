function drawDance() {
    gl.clearColor(0, 0, 1, 1)
    gl.clear(gl.COLOR_BUFFER_BIT)
    window.pending = requestAnimationFrame(drawDance)
}