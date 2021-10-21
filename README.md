# ユニットテストのサンプル

## 実行方法
ユニットテストを実行するには、このディレクトリの直下で、まず以下のコマンドを使って必要なpythonライブラリをインストールしてください。

```shell
$ pip install -r requirements.txt
```

その後、以下のコマンドを実行することでユニットテストを実行することができます。

```shell
$ python -m unittest
```

## 解説
### テスト対象モジュールの作成
このサンプルでユニットテストの対象にしているモジュールは、`main.py`に記述されています。  
このモジュールでは足し算を行う`sum_values`、ある数値が正の数であるかどうかを確認する`is_positive`、与えられた数の絶対値を返す`absolute`という3つの関数を実装しています。  

ここで、各関数に与えられる数値はスカラー値だけでなく、`numpy.ndarray`型で表現されるベクトルである可能性もあると仮定しましょう。  
そうした時、実装上は各関数をそれに対応し得るものにする必要があります。  
`sum_values`関数は、ベクトルの場合もスカラーの場合も、足し算は同じ演算子で実行されるので場合分けする必要がありませんが、
`is_positive`や`absolute`はベクトルが入ってきた場合に別の処理を行うように書く必要があります。

`absolute`は、入力がベクトルだった場合に限り、

```python
np.lingalg.norm(a)
```

と、L2ノルムを返却するように記述しています。

`is_positive`に関しては、この実装例ではわざと少し間違った実装をしています。  
本来は与えられた入力がベクトルだったときは、すべての成分が正であるかどうかを確認するようにしたいのですが、

```python
(a > 0).any()
```

と、ひとつでも正の成分が入っていれば真となるような実装になっています。

このような実装上のミスを発見するための方法のひとつとしてユニットテストが存在します。

### テストケースの作成
ユニットテストを行うためには、「テストケース」を書く必要があります。  
このサンプルでは、テストケースは`test_main.py`に記述されています。

中を覗いてみると、

```python
import unittest

import numpy as np

import main


class TestMain(unittest.TestCase):
    def test_sum_values_scalar(self):
        self.assertEqual(5, main.sum_values(2, 3))

    def test_sum_values_vector(self):
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        ret = main.sum_values(a, b)
        self.assertEqual(5, ret[0])
        self.assertEqual(7, ret[1])
        self.assertEqual(9, ret[2])

    def test_is_positive_all(self):
        all_positive = np.array([1, 2, 3])
        all_negative = np.array([-1, -2, -3])
        self.assertTrue(main.is_positive(all_positive))
        self.assertFalse(main.is_positive(all_negative))

    def test_is_positive_any(self):
        one_positive = np.array([1, -2, -3])
        self.assertFalse(main.is_positive(one_positive))

    def test_absolute_scalar(self):
        self.assertEqual(1, main.absolute(1))
        self.assertEqual(1, main.absolute(-1))
        self.assertEqual(0, main.absolute(0))

    def test_absolute_vector(self):
        self.assertEqual(5, main.absolute(np.array([4, 3])))
        self.assertEqual(5, main.absolute(np.array([-4, -3])))
```

となっています。

まず、1行目で`unittest`というモジュールをインポートしていることがわかりますが、pythonではこのモジュールを使ったユニットテストの実装がサポートされています。

ユニットテストを行うためのクラスを`unittest.TestCase`のサブクラスとして作成し、そのメンバとして`test_`で始まる名前のメソッドを実装していきます。

`self.assertEqual`や`self.assertTrue`といった関数を呼び出している部分が随所にありますが、
これは「2つの値が等しいかどうかを確認」したり、「ある値が真であるかどうかを確認」したりするためのものになります。  
より詳しいことは[公式ページ](https://docs.python.org/ja/3/library/unittest.html)をご参照ください。

ユニットテストのテストケースを書いていくにあたって大切なことは、十分なケースを網羅する点になります。  
例えば、今回あえて間違った実装にしている`is_positive`関数ですが、この実装でも次のテストケースは問題なく通過できます。

- `test_is_positive_all`
    - 要素すべてが正である場合
    - 要素すべてが負である場合

しかし、このテストだけでは実装にミスがあったことに気づくことができません。  
さらに次のテストケースを追加することで、「すべての要素が正であるかどうか」を正しく確認するための実装になっているかどうかをチェックすることができます。

- `test_is_positive_any`: 符号の入り混じった成分を持つベクトルに関して、ちゃんと偽を返せるかどうかを確認するためのテストケース

今回は非常に単純な演算の実装にとどまったため、まず見落とすことはないと思いますが、より複雑な処理をするようなプログラムを書いていく過程では、テストケースそのものを見落としてしまうこともしばしばあります。  
特に何か数理モデルの実装を行おうとする場合は、先に解析的にわかる性質をリストアップしておき、例えば振る舞いの変わるパラメータの周辺でのテストを記述してから実装に移ることで、モジュールの分割の仕方や実装の方針などが見えてくるようなケースもあるかもしれません。
