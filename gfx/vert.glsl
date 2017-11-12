#version 120
attribute vec3 pos;
attribute vec2 tex;
uniform vec3 trans;
uniform mat3 scale;
uniform mat3 rot;
uniform vec2 toff;
uniform vec2 tscale;
void main(){
vec3 wPos = (rot * scale * pos) + trans;
gl_Position = gl_ModelViewProjectionMatrix * vec4(wPos,1.0);
vec2 tpos = vec2((toff.x + tex.x)*tscale.x, (toff.y + tex.y)*tscale.y);
gl_FrontColor = vec4(tpos,1.0,1.0);
}