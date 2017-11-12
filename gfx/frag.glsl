#version 120
uniform sampler2D rentex;
uniform vec4 fog;
uniform vec4 col;
void main(){
gl_FragColor = mix(col*texture2D(rentex,vec2(gl_Color.x,-1*gl_Color.y)),vec4(fog.xyz,1.0),fog.w);
}