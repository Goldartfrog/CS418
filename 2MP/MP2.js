// File for interfacing the html to the javascript

function makeCanvasSize() {
    let canvas = document.querySelector('canvas')
    canvas.width = 500
    canvas.height = 500
    if (window.gl) {
        gl.viewport(0, 0, canvas.width, canvas.height)
    }
}


// Call the respective function depending on the radio button pressed

function radioChanged() {
    let chosen = document.querySelector('input[type="radio"]:checked').value
    cancelAnimationFrame(window.pending)
    window.pending = requestAnimationFrame(window['draw'+chosen])
}

// Adds listeners to the radio buttons
// also compiles, links, and sets up geometry

async function setup(event) {
    makeCanvasSize()
    document.querySelectorAll('input[type="radio"]').forEach(elem => {
        elem.addEventListener('change', radioChanged)
    })
    window.gl = document.querySelector('canvas').getContext('webgl2', {antialias: false, depth:true, preserveDrawingBuffer:true})
    let vs = await fetch('vert.glsl').then(res => res.text())
    let fs = await fetch('frag.glsl').then(res => res.text())
    window.program = compileAndLinkGLSL(vs, fs)
    gl.enable(gl.DEPTH_TEST)
    window.geom = setupGeomery(tetrahedron())
    window.addEventListener('resize', makeCanvasSize)
    radioChanged()
}


window.addEventListener('load',setup)
