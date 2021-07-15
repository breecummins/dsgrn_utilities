import subprocess
import DSGRN

subprocess.call("mpiexec -n 4 Signatures 2D_Example_A.txt 2D_test.db",shell=True)
subprocess.call("mpiexec -n 4 Signatures 3D_Haase_II.txt 3D_test.db",shell=True)

def test1():
    db2D1 = DSGRN.Database("2D_Example_A.db")
    db2D2 = DSGRN.Database("2D_test.db")
    for i in range(1600):
        assert db2D1(i) == db2D2(i)
    sqlexpression = "select * from MorseGraphAnnotations where MorseGraphIndex = ?"
    c = db2D1.cursor
    d = db2D2.cursor
    for i in range(77):
        c.execute(sqlexpression, (i,))
        ann1 = c.fetchall()
        d.execute(sqlexpression, (i,))
        ann2 = d.fetchall()
        assert ann1 == ann2
    subprocess.call("rm 2D_test.db",shell=True)


def test2():
    db3D1 = DSGRN.Database("3D_Haase_II.db")
    db3D2 = DSGRN.Database("3D_test.db")
    for i in range(40824):
        assert db3D1(i) == db3D2(i)
    sqlexpression = "select * from MorseGraphAnnotations where MorseGraphIndex = ?"
    c = db3D1.cursor
    d = db3D2.cursor
    for i in range(177):
        c.execute(sqlexpression, (i,))
        ann1 = c.fetchall()
        d.execute(sqlexpression, (i,))
        ann2 = d.fetchall()
        assert ann1 == ann2
    subprocess.call("rm 3D_test.db",shell=True)


if __name__ == "__main__":
    test1()





