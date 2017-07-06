#include <bits/stdc++.h>

using namespace std;

// This is a default checker
int main(int argc, char* argv[])
{
	//argv[1] for input file path
	//argv[2] for ouput file path
	//argv[3] for submission's output
	//1 in stdout means correct and 0 means wrong
    ifstream fin1, fin2;
    fin1.open(argv[2]);
    fin2.open(argv[3]);
    string s1,s2;
    while(fin1>>s1)
    {
    	if(fin2>>s2)
    	{
    		cout<<s1<<' '<<s2<<endl;
    		if(s1!=s2)
    		{
    			cout<<0<<endl;
    			return 0;
    		}
    		continue;
    	}
    	cout<<0<<endl;
    	return 0;
    }
    if(fin2>>s2)
    	cout<<0<<endl;
    else
    	cout<<1<<endl;
	return 0;
}