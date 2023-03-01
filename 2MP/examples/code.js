var tetrahedron =
    {"triangles":
        [4,5,6
        ,1,2,3
        ,2,3,0
        ,3,0,1
        ]
    ,"attributes":
        {"position":
            [[-0.5,-0.5,-0.5]
            ,[ 0.5, 0.5,-0.5]
            ,[-0.5, 0.5, 0.5]
            ,[ 0.5,-0.5, 0.5]
            ,[-0.5,-0.5,-0.5]
            ,[ 0.5, 0.5,-0.5]
            ,[-0.5, 0.5, 0.5]
            ]
        ,"vcolor":
            [[0,0,0]
            ,[1,1,1]
            ,[0,1,0]
            ,[1,0,1]
            ,[1,0,0]
            ,[1,0,0]
            ,[0,0,1]
            ]
        }
    }

function makeOtherGeom() {
    var g =
    {"triangles": []
    ,"attributes":
        {"position": []
        ,"vcolor": []
        }
    }
    for(let i=0; i<500; i+=1) {
        let cx = Math.random()*10-5, cy = Math.random()*10-5
        let cz = Math.random()*0.001
        g.attributes.position.push(
            [cx+Math.random(), -1+cz, cy+Math.random()],
            [cx+Math.random(), -1+cz, cy+Math.random()],
            [cx+Math.random(), -1+cz, cy+Math.random()],
        )
        g.triangles.push(
            g.attributes.position.length-3,
            g.attributes.position.length-2,
            g.attributes.position.length-1,
        )
        g.attributes.vcolor.push([1,0,0],[1,1,0],[1,0,0])
    }
    
    return g
}


/** Draw one frame */
function draw() {
    gl.clearColor(...IlliniBlue) // f(...[1,2,3]) means f(1,2,3)
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)
    gl.useProgram(program)

    gl.bindVertexArray(geom.vao)

    gl.uniform4fv(gl.getUniformLocation(program, 'color'), IlliniOrange)
    gl.uniformMatrix4fv(gl.getUniformLocation(program, 'mv'), false, m4mul(v,m1))
    gl.uniformMatrix4fv(gl.getUniformLocation(program, 'p'), false, p)
    gl.drawElements(geom.mode, geom.count, geom.type, 0)

    gl.uniformMatrix4fv(gl.getUniformLocation(program, 'mv'), false, m4mul(v,m2))
    gl.drawElements(geom.mode, geom.count, geom.type, 0)

    gl.uniformMatrix4fv(gl.getUniformLocation(program, 'mv'), false, m4mul(v,m3))
    gl.drawElements(geom.mode, geom.count, geom.type, 0)

    gl.bindVertexArray(geom2.vao)
    gl.uniformMatrix4fv(gl.getUniformLocation(program, 'mv'), false, v)
    gl.drawElements(geom2.mode, geom2.count, geom2.type, 0)
}

/** Compute any time-varying or animated aspects of the scene */
function timeStep(milliseconds) {
    let seconds = milliseconds / 1000;
    
    window.m1 = m4rotX(seconds)
    window.v = m4view([Math.cos(seconds/2),2,3], [0,0,0], [0,1,0])
    window.m3 = m4mul(m1, m4rotY(seconds), m4trans(0,2,0), m4scale(0.1,4,0.1))

    let when = seconds % 4
    let stage = Math.floor(when)
    let t = when - stage
    if (stage == 0) {
        window.m2 = m4trans(-1*t + 1*(1-t),0,1)
    } else if (stage == 1) {
        window.m2 = m4trans(-1,0,-1*t + 1*(1-t))
    } else if (stage == 2) {
        window.m2 = m4trans(1*t + -1*(1-t),0,-1)
    } else if (stage == 3) {
        window.m2 = m4trans(1,0,1*t + -1*(1-t))
    }

    draw()
    requestAnimationFrame(timeStep)
}

/** Resizes the canvas to completely fill the screen */
function fillScreen() {
    let canvas = document.querySelector('canvas')
    document.body.style.margin = '0'
    canvas.style.width = '100vw'
    canvas.style.height = '100vh'
    canvas.width = canvas.clientWidth
    canvas.height = canvas.clientHeight
    canvas.style.width = ''
    canvas.style.height = ''
    if (window.gl) {
        gl.viewport(0,0, canvas.width, canvas.height)
        window.p = m4perspNegZ(1, 10, 1.5, canvas.width, canvas.height)
    }
}

/** Compile, link, set up geometry */
async function setup(event) {
    window.gl = document.querySelector('canvas').getContext('webgl2',
        // optional configuration object: see https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
        {antialias: false, depth:true, preserveDrawingBuffer:true}
    )
    let vs = document.querySelector('#vert').textContent.trim()
    let fs = document.querySelector('#frag').textContent.trim()
    window.program = compileAndLinkGLSL(vs,fs)
    gl.enable(gl.DEPTH_TEST)
    window.geom = setupGeomery(tetrahedron)
    window.geom2 = setupGeomery(makeOtherGeom())
    fillScreen()
    window.addEventListener('resize', fillScreen)
    requestAnimationFrame(timeStep)
}

window.addEventListener('load',setup)