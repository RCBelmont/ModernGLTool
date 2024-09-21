#version 440

layout (local_size_x = 5, local_size_y = 1) in;
struct Vector4 {
    vec4 sh;
};

layout(std430, binding=0) buffer SHBuffer {
    Vector4 shData[];
} shBuffer;

layout(std430, binding=1) buffer OutputBuffer {
    Vector4 colorData[];
} outputBuffer;



vec3 GetSHDiffuse(vec3 Normal)
{
	vec4 NormalVector = vec4(Normal, 1.0f);

	vec3 Intermediate0, Intermediate1, Intermediate2;
	Intermediate0.x = dot(shBuffer.shData[0].sh, NormalVector);
	Intermediate0.y = dot(shBuffer.shData[1].sh, NormalVector);
	Intermediate0.z = dot(shBuffer.shData[2].sh, NormalVector);

	vec4 vB = NormalVector.xyzz * NormalVector.yzzx;
	Intermediate1.x = dot(shBuffer.shData[3].sh, vB);
	Intermediate1.y = dot(shBuffer.shData[4].sh, vB);
	Intermediate1.z = dot(shBuffer.shData[5].sh, vB);

	float vC = NormalVector.x * NormalVector.x - NormalVector.y * NormalVector.y;
	Intermediate2 = shBuffer.shData[6].sh.xyz * vC;

	// max to not get negative colors
	return max(vec3(0,0,0), Intermediate0 + Intermediate1 + Intermediate2);
}


void main()
{
    float time = gl_GlobalInvocationID.x / 4.0;
    vec3 normal = vec3(0, 1, mix(-1,1,time));
    normal = normalize(normal);
    vec3 color = GetSHDiffuse(normal);

    outputBuffer.colorData[gl_GlobalInvocationID.x].sh = vec4(color, time);
}