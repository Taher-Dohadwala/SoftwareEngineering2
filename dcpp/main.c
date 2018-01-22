#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifdef DEBUG
#define debugop() for (int x = 0; x < 6; x++) {printf("\t%f",heap[x]);};printf("\n");
#else
#define debugop() (void)0;
#endif


//printf("%f%c%f - > %d\n",heap[params[0]],c,heap[params[1]],params[2]);
int main() {
	char c;
	int tmp,params[3];
	params[0]=0;
	params[1]=0;
	params[2]=0;
	float *heap;
	while ((c=getchar())!='e') {
		switch (c) {
			case 'h':
				scanf("%d",&tmp);
				heap =(float*)malloc(sizeof(float)*tmp);
				break;
			case '0':
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
			case '9':
				ungetc(c,stdin);
				params[2] = params[1];
				params[1] = params[0];
				scanf("%d",&params[0]);
				break;
			case 'f':
				scanf("%f",&heap[params[0]]);
				#ifdef DEBUG
				printf("%f loaded\n",heap[params[0]]);
				#endif
				break;
			case '*':
				heap[params[2]]=heap[params[0]]*heap[params[1]];
				debugop();
				break;
			case '+':
				heap[params[2]]=heap[params[0]]+heap[params[1]];
				debugop();
				break;
			case '-':
				heap[params[2]]=heap[params[0]]-heap[params[1]];
				debugop();
				break;
			case '/':
				heap[params[2]]=heap[params[0]]/heap[params[1]];
				debugop();
				break;
			case '^':
				heap[params[2]]=pow(heap[params[0]],heap[params[1]]);
				debugop();
				break;
			case 'g':
				printf("%f\n",heap[params[0]]);

		}
	} 
}
