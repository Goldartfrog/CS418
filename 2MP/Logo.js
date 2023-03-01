function tetrahedron(){
    return {"triangles":
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
}
function drawLogo() {
    gl.clearColor(1, 0.373, 0.02, 1)
    gl.clear(gl.COLOR_BUFFER_BIT)
    window.pending = requestAnimationFrame(drawLogo)
}