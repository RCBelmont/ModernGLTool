 #version 430

 layout (local_size_x = 16, local_size_y = 16) in;
 layout(rgba8, location=0) uniform image2D destTex;



  void main()
  {
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(destTex);
    vec4 color = imageLoad(destTex, texelPos);
    //imageStore(destTex, texelPos, color);
    imageStore(destTex, texelPos, vec4(texelPos.x * 1.0f / (size.x * 1.0), 0, 0, 1));
    //imageStore(destTex, texelPos, vec4(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y, 0, 1));
  }