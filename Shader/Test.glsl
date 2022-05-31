 #version 430 core

 layout (local_size_x = 16, local_size_y = 16) in;
 layout(binding=0, rgba32f) readonly uniform image2D sourceTex;
 layout(binding=1, rgba32f) uniform image2D destTex;



  void main()
  {
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(destTex);
    vec4 color = imageLoad(sourceTex, texelPos);
    //imageStore(destTex, texelPos, color);
    float gray = dot(color.rgb,vec3(0.3, 0.59, 0.11));
    imageStore(destTex, texelPos, vec4(gray,gray,gray,1));
    //imageStore(destTex, texelPos, vec4(size, 0, 1));
    //imageStore(destTex, texelPos, vec4(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y, 0, 1));
  }