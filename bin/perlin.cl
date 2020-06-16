
#define lerp(t, a, b) ((a) + (t) * ((b) - (a)))

/*
float noise(int x, int y) {
    int n;

    n = x + y * 57;
    n = (n << 13) ^ n;
    return (1.0 - ((n * ((n * n * 15731) + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0);
}

__kernel void perlin_2D(__global float *dst, int width, int height, int offset,
                        float persistence, int octaves, int scale, float lacunarity) {
                        
    int index = get_global_id(0);
    int i, x, y;

    if (index >= width * height) {
        return;
    }

    x = index % width + offset;
    y = index / width + offset;
    
    float total = 0.0f;
    float frequency = 1.0f/(float)scale;
    float amplitude = persistence;

    for (i = 0; i < octaves; ++i)
    {
        total += noise(x * frequency, y * frequency) * amplitude;         
        frequency *= lacunarity;
        amplitude *= persistence;
    } 

    dst[index] = total;
}
*/

static inline float
grad2(const int hash, const float x, const float y)
{
    float GRAD3[][3] = {
	{1,1,0},{-1,1,0},{1,-1,0},{-1,-1,0}, 
	{1,0,1},{-1,0,1},{1,0,-1},{-1,0,-1}, 
	{0,1,1},{0,-1,1},{0,1,-1},{0,-1,-1},
	{1,0,-1},{-1,0,-1},{0,-1,1},{0,1,1}};
	const int h = hash & 15;
	return x * GRAD3[h][0] + y * GRAD3[h][1];
}

float noise2(float x, float y, const float repeatx, const float repeaty, const int base)
{
    unsigned char PERM[] = {
        151, 160, 137,  91,  90,  15, 131,  13, 201,  95,  96,  53, 194, 233,   7, 225, 140,
         36, 103,  30,  69, 142,   8,  99,  37, 240,  21,  10,  23, 190,   6, 148, 247, 120,
        234,  75,   0,  26, 197,  62,  94, 252, 219, 203, 117,  35,  11,  32,  57, 177,  33,
         88, 237, 149,  56,  87, 174,  20, 125, 136, 171, 168,  68, 175,  74, 165,  71, 134, 
        139,  48,  27, 166,  77, 146, 158, 231,  83, 111, 229, 122,  60, 211, 133, 230, 220, 
        105,  92,  41,  55,  46, 245,  40, 244, 102, 143,  54,  65,  25,  63, 161,   1, 216, 
         80,  73, 209,  76, 132, 187, 208,  89,  18, 169, 200, 196, 135, 130, 116, 188, 159,
         86, 164, 100, 109, 198, 173, 186,   3,  64,  52, 217, 226, 250, 124, 123,   5, 202,
         38, 147, 118, 126, 255,  82,  85, 212, 207, 206,  59, 227,  47,  16,  58,  17, 182, 
        189,  28,  42, 223, 183, 170, 213, 119, 248, 152,   2,  44, 154, 163,  70, 221, 153, 
        101, 155, 167,  43, 172,   9, 129,  22,  39, 253,  19,  98, 108, 110,  79, 113, 224, 
        232, 178, 185, 112, 104, 218, 246,  97, 228, 251,  34, 242, 193, 238, 210, 144,  12, 
        191, 179, 162, 241,  81,  51, 145, 235, 249,  14, 239, 107,  49, 192, 214,  31, 181, 
        199, 106, 157, 184,  84, 204, 176, 115, 121,  50,  45, 127,   4, 150, 254, 138, 236,
        205,  93, 222, 114,  67,  29,  24,  72, 243, 141, 128, 195,  78,  66, 215,  61, 156, 
        180, 151, 160, 137,  91,  90,  15, 131,  13, 201,  95,  96,  53, 194, 233,   7, 225,
        140,  36, 103,  30,  69, 142,   8,  99,  37, 240,  21,  10,  23, 190,   6, 148, 247, 
        120, 234,  75,   0,  26, 197,  62,  94, 252, 219, 203, 117,  35,  11,  32,  57, 177, 
         33,  88, 237, 149,  56,  87, 174,  20, 125, 136, 171, 168,  68, 175,  74, 165,  71, 
        134, 139,  48,  27, 166,  77, 146, 158, 231,  83, 111, 229, 122,  60, 211, 133, 230, 
        220, 105,  92,  41,  55,  46, 245,  40, 244, 102, 143,  54,  65,  25,  63, 161,   1, 
        216,  80,  73, 209,  76, 132, 187, 208,  89,  18, 169, 200, 196, 135, 130, 116, 188, 
        159,  86, 164, 100, 109, 198, 173, 186,   3,  64,  52, 217, 226, 250, 124, 123,   5, 
        202,  38, 147, 118, 126, 255,  82,  85, 212, 207, 206,  59, 227,  47,  16,  58,  17, 
        182, 189,  28,  42, 223, 183, 170, 213, 119, 248, 152,   2,  44, 154, 163,  70, 221, 
        153, 101, 155, 167,  43, 172,   9, 129,  22,  39, 253,  19,  98, 108, 110,  79, 113, 
        224, 232, 178, 185, 112, 104, 218, 246,  97, 228, 251,  34, 242, 193, 238, 210, 144, 
         12, 191, 179, 162, 241,  81,  51, 145, 235, 249,  14, 239, 107,  49, 192, 214,  31, 
        181, 199, 106, 157, 184,  84, 204, 176, 115, 121,  50,  45, 127,   4, 150, 254, 138, 
        236, 205,  93, 222, 114,  67,  29,  24,  72, 243, 141, 128, 195,  78,  66, 215,  61, 
        156, 180};
        
	float fx, fy;
	int A, AA, AB, B, BA, BB;
	int i = (int)floor(fmod(x, repeatx));
	int j = (int)floor(fmod(y, repeaty));
	int ii = (int)fmod(i + 1, repeatx);
	int jj = (int)fmod(j + 1, repeaty);
	i = (i & 255) + base;
	j = (j & 255) + base;
	ii = (ii & 255) + base;
	jj = (jj & 255) + base;

	x -= floor(x); y -= floor(y);
	fx = x*x*x * (x * (x * 6 - 15) + 10);
	fy = y*y*y * (y * (y * 6 - 15) + 10);

	A = PERM[i];
	AA = PERM[A + j];
	AB = PERM[A + jj];
	B = PERM[ii];
	BA = PERM[B + j];
	BB = PERM[B + jj];
		
	return lerp(fy, lerp(fx, grad2(PERM[AA], x, y),
							 grad2(PERM[BA], x - 1, y)),
					lerp(fx, grad2(PERM[AB], x, y - 1),
							 grad2(PERM[BB], x - 1, y - 1)));
}

__kernel void perlin_2D(__global float *dst, int octaves, float persistence,
                        float lacunarity, int width, int height, int base, float scale) {
	//float x, y;
	//int octaves = 1;
	//float persistence = 0.5f;
    //float lacunarity = 2.0f;
	//float width = 1024; // arbitrary
	//float height = 1024; // arbitrary
	//int base = 0;

    int index = get_global_id(0);
    int i; 
    float x, y;

    if (index >= width * height) {
        return;
    }

    x = ((float)(index % width)) / scale;
    y = ((float)(index / width)) / scale;

    float freq = 1.0f;
    float amp = 1.0f;
    float max = 0.0f;
    float total = 0.0f;

    for (i = 0; i < octaves; i++) {
        total += noise2((float)x * freq, (float)y * freq, (float)width * freq, (float)height * freq, base) * amp;
        max += amp;
        freq *= lacunarity;
        amp *= persistence;
    }
    
    dst[index] = total/max;// / max;
    //dst[index] = (float)index / (width * height);
}
