import suite as st
import dvtDecimal as dD
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)


u = []
u.append(st.suite(fonction=lambda x: x+2))

u.append(st.suite(p_terme=(1, 110),
                  fonction=lambda x: 5*x-dD.dvtDecimal(2, 3),
                  rec=True))

f = lambda x: x * 5
u.append(st.suite(rang_p_terme=1, fonction=f))

u.append(st.suite(fonction=lambda x: 3 ** x))

for S in u:
    print(S)
    for i in S.on_demand(10, approx=False):
        print(i)
    S.get_terme_rang(1)
    S.get_terme_rang(8)
    print(S.termes_connus)
    S.play()
    # print(S.get_diff_succ())
    # print(S.get_div_succ())
    # print(S.get_somme_premiers(3))
    listes = S.get_rep_rec(5)
    l, m = listes
    N = 200
    debut = 0
    fin = 1
    x = debut
    X = []
    Y = []
    # for i in range(N + 1):
    #     X += [x]
    #     Y += [fonction(x)]
    #     x += (fin - debut) / N
    # plt.plot(X, Y, color="red")
    for i in range(0, len(l), 3):
        plt.plot(l[i:i+3], m[i:i+3],
                 color="blue",
                 linewidth=1,
                 dashes=(3, 1))
        etiq = r'$u_{' + str(i//3) + r'}$'
        # plt.text(l[i], -.05,
        #          ha='center',
        #          fontsize=15,
        #          color="blue",
        #          s=etiq)
    listes = S.get_rep_exp(5)
    l, m = listes
    plt.scatter(*listes, color='red')
    ax = plt.gca()
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.show()
