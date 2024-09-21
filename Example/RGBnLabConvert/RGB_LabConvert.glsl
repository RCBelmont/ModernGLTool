#version 440
layout (local_size_x = 1, local_size_y = 1) in;
//layout(binding=1, rgba32f) uniform image2D dstTex;
uniform vec4 srcColor;

layout(std430, binding=1) buffer OutputBuffer {
    vec4 colorData[];
} outputBuffer;

vec3 RGBToXYZ(vec3 RGB){
    vec3 XYZ = vec3(0);
    float var_R = RGB.r;
    float var_G = RGB.g;
    float var_B = RGB.b;

    //Observer. = 2°, Illuminant = D65
    float X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805;
    float Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722;
    float Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505;


    return vec3(X,Y,Z);
}

vec3 XYZToRGB(vec3 XYZ){
    float var_X = XYZ.x;
    float var_Y = XYZ.y;
    float var_Z = XYZ.z;
    float var_R = var_X *  3.2406 + var_Y * -1.5372 + var_Z * -0.4986;
    float var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415;
    float var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570;
    return vec3(var_R, var_G, var_B);
}

vec3 XYZToLab(vec3 XYZ){
    float var_X = XYZ.x / 0.95047;//ref_X =  95.047   Observer= 2°, Illuminant= D65
    float var_Y = XYZ.y / 1.0;//ref_Y = 100.000
    float var_Z = XYZ.z / 1.0883;//ref_Z = 108.883

    if (var_X > 0.008856) {
        var_X = pow(var_X, (1.0/3.0));
    }
    else {
        var_X = (7.787 * var_X) + (16.0/ 116.0);
    }


    if (var_Y > 0.008856){
        var_Y = pow(var_Y, (1.0/3.0));
    } else {
        var_Y = (7.787 * var_Y) + (16.0 / 116.0);
    }

    if (var_Z > 0.008856){
        var_Z = pow(var_Z, (1.0/3.0));
    } else {
        var_Z = (7.787 * var_Z) + (16.0 / 116.0);
    }

    float CIE_L = (116 * var_Y) - 16;
    float CIE_a = 500 * (var_X - var_Y);
    float CIE_b = 200 * (var_Y - var_Z);
    return vec3(CIE_L/100.0, CIE_a/127.0, CIE_b/127.0);
}

vec3 LabToXYZ(vec3 Lab){
    float CIE_L = Lab.x*100.0;
    float CIE_a = Lab.y*127.0;
    float CIE_b = Lab.z*127.0;

    float var_Y = (CIE_L + 16) / 116;
    float var_X = CIE_a / 500.0 + var_Y;
    float var_Z = var_Y - CIE_b / 200;




    if (pow(var_Y, 3.0) > 0.008856){
        var_Y = pow(var_Y, 3.0);
    }
    else {
        var_Y = (var_Y - 16.0 / 116.0) / 7.787;
    }
    if (pow(var_X, 3.0) > 0.008856){
        var_X = pow(var_X, 3.0);
    }
    else {
        var_X = (var_X - 16.0 / 116.0) / 7.787;
    }
    if (pow(var_Z, 3.0) > 0.008856) {
        var_Z = pow(var_Z, 3.0);
    }
    else {
        var_Z = (var_Z - 16.0 / 116.0) / 7.787;
    }

    float X = var_X * 0.95047;//ref_X =  95.047     Observer= 2°, Illuminant= D65
    float Y = var_Y * 1.0;//ref_Y = 100.000
    float Z = var_Z * 1.0883;//ref_Z = 108.883


    return vec3(X, Y, Z);
}




void main()
{
    //    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    //    ivec2 size = imageSize(dstTex);


    vec3 xyz = RGBToXYZ(srcColor.rgb);
    vec3 lab = XYZToLab(xyz);
    vec4 out_color = vec4(lab.rgb, 1);


    outputBuffer.colorData[0] = vec4(lab.rgb, 1);

    //0.53232884 0.6307819  0.52922523
    //0.87737036 -0.6786193   0.65484756
    outputBuffer.colorData[1] = vec4(XYZToRGB(LabToXYZ(vec3(1,-1,-1))), 1);

    //    imageStore(dstTex, texelPos, out_color);
}