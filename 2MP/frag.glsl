#version 300 es
precision highp float;
uniform vec4 color;
in vec4 fcolor;
out vec4 fragColor;
void main() {
    fragColor = fcolor;
}