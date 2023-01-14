#version 330

#define NR_TEXTURES 32

in float v_tex;
in vec2 v_uv;

struct TexProfile {
    sampler2D s;
};

uniform TexProfile textures[NR_TEXTURES];

out vec4 f_color;

void main() {
    int index = int(v_tex);
    f_color = texture(textures[index].s, v_uv);
}