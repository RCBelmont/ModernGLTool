 #version 430 core

 layout (local_size_x = 16, local_size_y = 16) in;
 layout(location=0) uniform sampler2D texture0;
 layout(binding=1, rgba32f) uniform image2D destTex;



  // void main()
  // {
  //   ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
  //   ivec2 size = imageSize(destTex);
  //   vec4 color = imageLoad(destTex, texelPos);
  //   //imageStore(destTex, texelPos, color);
  //   float gray = dot(color.rgb,vec3(0.0, 0.59, 0.0));
  //   vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
  //   vec4 c = texture(texture0, uv);
  //   imageStore(destTex, texelPos, vec4(c.rgb,1));
  //   //imageStore(destTex, texelPos, vec4(size, 0, 1));
  //   //imageStore(destTex, texelPos, vec4(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y, 0, 1));
  // }

  void main()
  {
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(destTex);
    vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
    vec2 cood = (uv - 0.5) * 2;
    vec4 color = texture(texture0, uv);
    float l = length(cood) * length(cood);
    float v = sqrt(0.8 - l*l);
    float b_alpha = 1-color.a;
    vec4 out_color = vec4(color.r*color.a + b_alpha, color.g*color.a + b_alpha, color.b*color.a + b_alpha, 1);
    imageStore(destTex, texelPos, out_color);
  }