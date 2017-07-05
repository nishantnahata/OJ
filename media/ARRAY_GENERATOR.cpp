#include <bits/stdc++.h>
#define ff first
#define se second
#define pb push_back
#define nn 6000
#define mt make_tuple
#define mp make_pair
#define ll long long int
#define db double
#define ldb long double
#define inf 1000000000000000000ll
#define logn 20
#define mod 1000000007ll
#define mod1 mod
#define mod2 100000009ll
#define sqr(a) a*1ll*a
#define nullp mp(-1,-1)
#define set0(a) memset(a,0,sizeof a)
#define init(a) memset(a,-1,sizeof a)
#define cmp 1e-16
 
using namespace std;

typedef pair<int,int> pii;

int pr[]={2,3,5,7,11,13,17,19,23,29,31,37};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    #ifndef ONLINE_JUDGE
    freopen("input.txt","r",stdin);
    freopen("input.txt","w",stdout);
    #endif
	int t=1;
	srand((unsigned)time(0));
	//cout<<t<<endl;
	while(t--)
	{
		int n=100000;
		cout<<n<<endl;
		for(int i=0;i<n;i++)
		{
			int a = (rand()%10) + 1;
			cout<<a<<' ';
		}
		cout<<endl;
	}
    return 0;
}