#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "gdx2d.h"

int main (int argc, char *argv[]) {
	char *fname;
	FILE *fp;
	unsigned int fsize;
	char *buf;

	if (argc<2) {
		printf("usage: %s filename\n",argv[0]);
		return -1;
	}

	fname = strdup(argv[1]);
	fp = fopen(fname, "rb");
	fseek(fp, 0, SEEK_END);
	fsize = ftell(fp);
	fseek(fp, 0, SEEK_SET); 

	printf("reading file %s, %d bytes\n",fname,fsize);

	buf = malloc(fsize + 1);
	memset(buf,0,fsize + 1);

	fread(buf, fsize, 1, fp);
	fclose(fp);

	gdx2d_load(buf,fsize);
	return 0;
}
