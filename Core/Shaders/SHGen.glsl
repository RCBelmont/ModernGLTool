#version 440
layout (local_size_x = 9, local_size_y = 1) in;
struct MyData {
    vec4 coff;
};

layout(std430, binding = 0) buffer MyBuffer {
    MyData data[];
} myBuffer;


//vec4 light_list[] = { vec4(0.6510, 0.505, 0.52255, 0.30) * vec4(.6, .6, .6, 1), vec4(0.6510, 0.60, 0.52255, 0.35) * vec4(1.1, 1.1, 1.1, 1), vec4(0.625, 0.6059, 0.5859, 0.7)*vec4(1.5, 1.5, 1.5, 1), vec4(0.648, 0.647, 0.726, 1)*vec4(1.0, 1.0, 1.0, 1) };

//vec4 light_list[] = {vec4(0.0819, 0.0715, 0.08854, 0.2)* vec4(.2,.1,.4,1), vec4(0.0819, 0.0715, 0.08854, 0.3), vec4(0.5625, 0.53317, 0.5214, 0.72)* vec4(1.2,1.2,1.2,1), vec4(1, 1, 1, 1) };
vec4 light_list[] = { vec4(1, 0, 0, 0.2), vec4(0, 0., 0, 0.6), vec4(0, 0, 0, 1) };

vec4 bottom_light3 = vec4(0, 0, 1, 1.000000);



const float HrizontalRange1 = 0.4;
const float HrizontalRange2 = -0.2;



vec3 spherical_uniform_sampling(int num_samples, float seed)
{
    float phi = seed * 2.0 * 3.14159;
    float theta = acos(1.0 - 2.0 * seed);

    float x = sin(theta) * cos(phi);
    float y = sin(theta) * sin(phi);
    float z = cos(theta);

    return vec3(x, y, z);
}


vec3 get_cubemap_vector(vec2 co, int face)
{
  /* NOTE(Metal): Declaring constant array in function scope to avoid increasing local shader
   * memory pressure. */
  const mat3 CUBE_ROTATIONS[6] = mat3[](
      mat3(vec3(0.0, 0.0, -1.0), vec3(0.0, -1.0, 0.0), vec3(-1.0, 0.0, 0.0)),
      mat3(vec3(0.0, 0.0, 1.0), vec3(0.0, -1.0, 0.0), vec3(1.0, 0.0, 0.0)),
      mat3(vec3(1.0, 0.0, 0.0), vec3(0.0, 0.0, 1.0), vec3(0.0, -1.0, 0.0)),
      mat3(vec3(1.0, 0.0, 0.0), vec3(0.0, 0.0, -1.0), vec3(0.0, 1.0, 0.0)),
      mat3(vec3(1.0, 0.0, 0.0), vec3(0.0, -1.0, 0.0), vec3(0.0, 0.0, -1.0)),
      mat3(vec3(-1.0, 0.0, 0.0), vec3(0.0, -1.0, 0.0), vec3(0.0, 0.0, 1.0)));
  return normalize(CUBE_ROTATIONS[face] * vec3(co * 2.0 - 1.0, 1.0));
}

void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    int comp = texelPos.x;
    int slice = 64;
    float PI = 3.1415926;
    float PI_2 = 2.0 * PI;
    vec3 coff_temp = vec3(0);
    int acc_count = 0;
    for (int f= 0; f <6; f++){
        for (int i = 0; i < slice; i++){
            for (int j = 0; j<slice; j++){
                float coef;
                float theta = acos(sqrt(1-(float(j)/(slice-1.0))));//(float(j)/(slice-1.0)) * PI;
                float phi = (float(i)/(slice-1.0)) * PI*2.0;
                vec3 cubevec = get_cubemap_vector(vec2(float(i)/slice, float(j)/slice), f);
                // float count1 = i*slice + j;
                //vec3 cubevec = spherical_uniform_sampling(1024*1024, count1/slice*slice);
                cubevec = normalize(cubevec);
                float t = (cubevec.z + 1) * 0.5;

                vec3 cube_color = vec3(0);
                for (int k=0; k<3;k++){
                    if (t <= light_list[k].a){
                        cube_color = light_list[k].rgb;
                        break;
                    }
                }
                cube_color = vec3(1, 0, 0);

                cubevec = vec3(cubevec.x, cubevec.z, cubevec.y);
                cubevec = normalize(cubevec);
                if (comp == 0) {
                    coef = 0.282095;
                }
                else if (comp == 1) {
                    coef = -0.488603 * cubevec.z * 2.0 / 3.0;
                }
                else if (comp == 2) {
                    coef = 0.488603 * cubevec.y * 2.0 / 3.0;
                }
                else if (comp == 3) {
                    coef = -0.488603 * cubevec.x * 2.0 / 3.0;
                }
                else if (comp == 4) {
                    coef = 1.092548 * cubevec.x * cubevec.z * 1.0 / 4.0;
                }
                else if (comp == 5) {
                    coef = -1.092548 * cubevec.z * cubevec.y * 1.0 / 4.0;
                }
                else if (comp == 6) {
                    coef = 0.315392 * (3.0 * cubevec.y * cubevec.y - 1) * 1.0 / 4.0;
                }
                else if (comp == 7) {
                    coef = -1.092548 * cubevec.x * cubevec.y * 1.0 / 4.0;
                }
                else { /* (comp == 8) */
                    coef = 0.546274 * (cubevec.x * cubevec.x - cubevec.z * cubevec.z) * 1.0 / 4.0;
                }


                //            if (comp == 0) {
                //                 coef = 0.282095 * 0.282095;
                //            }
                //            else if (comp == 1) {
                //                coef = -0.488603 * -0.488603 * cubevec.y * 2.0 / 3.0;
                //
                //            }
                //            else if (comp == 2) {
                //                coef = 0.488603 * 0.488603 * cubevec.z * 2.0 / 3.0;
                //            }
                //            else if (comp == 3) {
                //
                //                coef = -0.488603 * -0.488603 * cubevec.x * 2.0 / 3.0;
                //            }
                //            else if (comp == 4) {
                //                coef = 1.092548 * 1.092548 * cubevec.x * cubevec.y * 1.0 / 4.0;
                //            }
                //            else if (comp == 5) {
                //                coef = -1.092548* -1.092548 * cubevec.y * cubevec.z * 1.0 / 4.0;
                //            }
                //            else if (comp == 6) {
                //                coef = 0.315392 * (3.0 * cubevec.z * cubevec.z - 1.0) * 1.0 / 4.0;
                //            }
                //            else if (comp == 7) {
                //                coef = -1.092548 * -1.092548 * cubevec.x * cubevec.z * 1.0 / 4.0;
                //            }
                //            else { /* (comp == 8) */
                //                coef = 0.546274 * 0.546274 * (cubevec.x * cubevec.x - cubevec.y * cubevec.y) * 1.0 / 4.0;
                //            }

                coff_temp += cube_color * coef;
                acc_count += 1;

            }
        }
    }
    coff_temp *= (4.0*PI/ acc_count);

    myBuffer.data[texelPos.x].coff = vec4(coff_temp, 0);
}