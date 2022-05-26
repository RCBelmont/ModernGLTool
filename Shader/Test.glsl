 #version 430

 layout (local_size_x = 16, local_size_y = 16) in;
 layout(rgba8, location=0) writeonly uniform image2D destTex;



  void main()
  {
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(destTex);
    imageStore(destTex, texelPos, vec4(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y, 0, 1));
  }