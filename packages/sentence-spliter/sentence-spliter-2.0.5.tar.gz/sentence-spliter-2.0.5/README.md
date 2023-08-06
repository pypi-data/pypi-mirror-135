# sentence-spliter

[toc]

## 1. 介绍

sentence-spliter 句子切分工具，将一个长的句子，切分为短句的 List 。支持自然切分，最长句切分，最短句合并。

目前支持语言：中文， 英文



## 2. 项目结构

```bash

├── README.md
├── automata             	# 存放切句的基本单元
│   ├── abs.py            	# 定义状态机与图的基本单元
│   ├── condition.py		 	# 切句条件
│   ├── operation.py     	    # 切句操作
│   ├── sequence.py			# 封装状态传递的数据
│   ├── state_machine.py      # 状态机
│   ├──  self.symbols.py  # 保存标点符号
│   ├── weights_list.py   # 英文短句切割 权重名单 (优先截断并列句，重句)
│   └── white_list.py     # 英文短句白名单 e.g. Mr. U.S. Ph.D
└── sentence_spliter
    ├── logic_graph.py     # 逻辑图(中文)
    ├── logic_graph_en.py  # 逻辑图(英文)
    └── spliter.py		 # 主要函数，调用切句

```


## 3. Setup

PYPI 安装

```
pip install sentence_spliter
```

## 4. Demo

### 4.1. Simple Demo

```python
from sentence_spliter_old import spliter

# 中文切句调用 cut_to_sentences
paragraph = "在很久很久以前......。。... 有座山，山里有座庙啊!!!!!!!庙里竟然有个老和尚！？。。。。"
result = spliter.cut_to_sentences(paragraph)
print(result)

# outputs
['在很久很久以前......。。...', ' 有座山，山里有座庙啊!!!!!!!', '庙里竟然有个老和尚！？。。。。']
```

切句支持以整片文章为输入。

如果输入太长，终端会自动显示百分比`process cutting 87.5%`

```python
from sentence_spliter_old import spliter

paragraph = "A long time ago..... there is a mountain, and there is a temple in the mountain!!! And here is an old monk in the temple!?...."
result = spliter.cut_to_sentences_en(paragraph)

# outputs 
['A long time ago..... there is a mountain, and there is a temple in the mountain!!!',
 ' And here is an old monk in the temple!?....']
```

### 4.2 中文切句逻辑

中文 切句工具默认有三种逻辑

#### 4.2.1. 简单切句

```python
from sentence_spliter_old.logic_graph import simple_cuter
from sentence_spliter_old.automata.state_machine import StateMachine
from sentence_spliter_old.automata.sequence import StrSequence

# -- 初始化 状态机器 -- #
cuter = StateMachine(simple_cuter())

# -- 处理句子 -- #
paragraph = "在很久很久以前1.2.3......。。... 有座山。山里有座庙啊!!!!!!!庙里竟然有个老和尚！？。。。。www.baidu.com"
sequence = cuter.run(StrSequence(paragraph))
out = sequence.sentence_list()

# -- 展示结果 -- #
print(out)

# outputs
['在很久很久以前1.2.3......。。...', ' 有座山。', '山里有座庙啊!!!!!!!', '庙里竟然有个老和尚！？。。。。', 'www.baidu.com']
```

基本逻辑：

> - 遇到断句标点（。？！）准备切句：
>   - 如果短句标点出现在`引号`  、`括号`、`书名号`不执行切句
>   - 其他情况下执行切句

#### 4.2.2. 长短处理切句

```python
from sentence_spliter_old.logic_graph import long_short_cuter
from sentence_spliter_old.automata.state_machine import StateMachine
from sentence_spliter_old.automata.sequence import StrSequence

# -- 初始化 状态机器 -- #
cuter = StateMachine(long_short_cuter(hard_max=128, max_len=128, min_len=15))

# -- 处理句子 -- #
paragraph = "在很久很久以前1.2.3......。。... 有座山。山里有座庙啊!!!!!!!庙里竟然有个老和尚！？。。。。www.baidu.com"
sequence = cuter.run(StrSequence(paragraph))
out = sequence.sentence_list()

# -- 展示结果 -- #
print(out)
['在很久很久以前1.2.3......。。...', ' 有座山。山里有座庙啊!!!!!!!', '庙里竟然有个老和尚！？。。。。', 'www.baidu.com']
```

```python
from sentence_spliter_old.logic_graph import long_short_cuter
from sentence_spliter_old.automata.state_machine import StateMachine
from sentence_spliter_old.automata.sequence import StrSequence

# -- 初始化 状态机器 -- #
cuter = StateMachine(long_short_cuter(hard_max=2, max_len=2, min_len=1))

# -- 处理句子 -- #
paragraph = "在很久很久以前1.2.3......。。... 有座山。山里有座庙啊!!!!!!!庙里竟然有个老和尚！？。。。。www.baidu.com"
sequence = cuter.run(StrSequence(paragraph))
out = sequence.sentence_list()

# -- 展示结果 -- #
print(out)
['在很', '久很', '久以', '前1', '.2', '.3', '..', '..', '..', '。。', '..', '.', ' 有', '座山', '。', '山里', '有座', '庙啊', '!!', '!!',
 '!!', '!', '庙里', '竟然', '有个', '老和', '尚！', '？。', '。。', '。', 'ww', 'w.', 'ba', 'id', 'u.', 'com']
```

需要参数：

> - hard_max （默认300）: 最大可接受长度，要保证所有句子（除了最后一句）<= hard_max
> - max_len （默认128）: 长句判断条件，如果句子大于 max_len则为长句
>   - max_len 可以等于 hard_max
> - min_len （默认15）: 短句判断条件，如果句子小于min_len则为短句

基本逻辑：

> - 如果是短句：则该句子与右边句子合并
> - 如果是长句：
>   - 优先基于断句标点做二次切句
>   - 再

```python
from sentence_spliter_old.logic_graph import long_short_cuter
from sentence_spliter_old.automata.state_machine import StateMachine
from sentence_spliter_old.automata.sequence import StrSequence

# -- 初始化 状态机器 -- #
cuter = StateMachine(long_short_cuter(hard_max=128, max_len=128, min_len=15))

# -- 处理句子 -- #
paragraph = "“我和你讨论的不是一个东西，死亡率与死亡比例是不同的”“你知道么？CNN你们总是制造假新闻。。。”"
sequence = cuter.run(StrSequence(paragraph))
out = sequence.sentence_list()

# -- 展示结果 -- #
print(out)
['“我和你讨论的不是一个东西，死亡率与死亡比例是不同的”', '“你知道么？CNN你们总是制造假新闻。。。”']

# -- 处理句子 -- #
paragraph = "“我和你讨论的不是一个东西，死亡率与死亡比例是不同的”      “你知道么？CNN你们总是制造假新闻。。。”"
sequence = cuter.run(StrSequence(paragraph))
out = sequence.sentence_list()

# -- 展示结果 -- #
print(out)
['“我和你讨论的不是一个东西，死亡率与死亡比例是不同的”', '“你知道么？CNN你们总是制造假新闻。。。”']

# -- 处理句子 -- #
paragraph = "张晓风笑着说道，“我们这些年可比过去强多了！“过去吃不起饭，穿不暖衣服。 现在呢？要啥有啥！"
sequence = cuter.run(StrSequence(paragraph))
out = sequence.sentence_list()

# -- 展示结果 -- #
print(out)
['张晓风笑着说道，“我们这些年可比过去强多了！', '“过去吃不起饭，穿不暖衣服。 现在呢？要啥有啥！']
```

基本逻辑：

> 除了支持长短句以外，增加`双引号`处理特殊规则
>
> 1. 右边引号后面跟有左引号，切句
> 2. 中文中只有做引号，从第二个做引号开始切句
> 

### 4.3 英文切句逻辑

英文 切句目前只有一种逻辑

#### 4.3.2 长短句处理

短句展示 demo

```python
from sentence_spliter_old.logic_graph_en import long_cuter_en
from sentence_spliter_old.automata.state_machine import StateMachine
from sentence_spliter_old.automata.sequence import EnSequence  # 调取英文 Sequence

# -- 初始化 状态机 -- #
__long_machine_en = StateMachine(long_cuter_en(min_len=5))  # 令句子长度不能小于10个单词

# --- 处理句子 --- #
paragraph = "A long time ago. there is a mountain, and there is a temple in the mountain!!! And here is an old monk in the temple!?...."
m_input = EnSequence(paragraph)
__long_machine_en.run(m_input)

# -- output -- #
# ['A long time ago. there is a mountain, and there is a temple in the mountain!!!', ' And here is an old monk in the temple!?....']
# 可以看到 long time ago. 并没有被切开

# -- 改变句子最小长度 -- #
__long_machine_en = StateMachine(long_cuter_en(min_len=4))  # 令句子长度不能小于4个单词
paragraph = "A long time ago. there is a mountain, and there is a temple in the mountain!!! And here is an old monk in the temple!?...."
m_input = EnSequence(paragraph)
__long_machine_en.run(m_input)

# -- output -- #
# ['A long time ago.', ' there is a mountain, and there is a temple in the mountain!!!', ' And here is an old monk in the temple!?....']
# 可以看到 long time ago. 被切开
```

长句demo

```python
from sentence_spliter_old.logic_graph_en import long_cuter_en
from sentence_spliter_old.automata.state_machine import StateMachine
from sentence_spliter_old.automata.sequence import EnSequence  # 调取英文 Sequence

# -- 初始化 状态机 -- #
__long_machine_en = StateMachine(long_cuter_en(max_len=12, min_len=3))  # 令句子长度不能小于3个单词，并且不能大于12个单词

# -- 处理句子 -- #
paragraph = "A long time ago. there is a mountain, and there is a temple in the mountain!!! And here is an old monk in the temple!?...."
m_input = EnSequence(paragraph)
__long_machine_en.run(m_input)

# -- output -- #
# ['A long time ago.', ' there is a mountain, and there is a temple in the mountain!!!', ' And here is an old monk in the temple!?....']
# 可以看到中间句子并咩有被切开


# -- 改变句子最大长度 -- #
__long_machine_en = StateMachine(long_cuter_en(max_len=11, min_len=3))  # 令句子长度不能小于3个单词，并且不能大于12个单词
paragraph = "A long time ago. there is a mountain, and there is a temple in the mountain!!! And here is an old monk in the temple!?...."
m_input = EnSequence(paragraph)
__long_machine_en.run(m_input)

# -- output -- #
# ['A long time ago.', ' There is a mountain, ', 'and there is a temple in the mountain!!! And here is an old monk in the temple!?....']
# 可以看到中间句子被切成了两个
```

长句切除优先级 切除对话中的句子>切除并列句子>切除从句 如果以上都不满足，不切句

```python
from sentence_spliter_old.logic_graph_en import long_cuter_en
from sentence_spliter_old.automata.state_machine import StateMachine
from sentence_spliter_old.automata.sequence import EnSequence  # 调取英文 Sequence

sentence = "\"What would a stranger do here, Mrs. Price?\" he inquired angrily, remembering, with a pang, that certain new, unaccountable, engrossing emotions had quite banished Fiddy from his thoughts and notice, when he might have detected the signs of approaching illness, met them and vanquished them before their climax."
__long_machine_en = StateMachine(long_cuter_en(max_len=9, min_len=3))
m_input = EnSequence(sentence)
__long_machine_en.run(m_input)
for v in m_input.sentence_list():
    print(v)

# 输出
'''
"What would a stranger do here, Mrs. Price?" 
he inquired angrily, remembering, with a pang, 
that certain new, unaccountable, engrossing emotions had quite banished Fiddy from his thoughts and notice, 
when he might have detected the signs of approaching illness, 
met them and vanquished them before their climax.
'''
# 可以看到 优先切割 对话，其次从句， 最后是'，'
```

#### 4.3.3 英文白名单
切句会照护一些特殊缩写，e.g. U.S.A 这类词是不会被切句。 我们的白名单全部来自于《牛津词典第八版本》用户也可以通过修改white_list.py增加白名单内容

```python
from sentence_spliter_old.spliter import cut_to_sentences_en

sentence = "Notice that U.S.A. can also be written USA, but U.S. is better with the periods. Also, we can use U.S. as a modifier (the U.S. policy on immigration) but not as a noun (He left the U.S. U.S.A.)."
out = cut_to_sentences_en(sentence)
for v in out:
    print(v)

'''
Notice that U.S.A. can also be written USA, but U.S. is better with the periods.
Also, we can use U.S. as a modifier (the U.S. policy on immigration) but not as a noun (He left the U.S. U.S.A.).
'''
```

## 5. 自定义规则

切句规则都是基于图来实现的，其中

- `automata/condition.py` 存放图的边
- `automata/operation.py` 存放节点

### 5.1. 定义一个简单的切句规则

规则如下：

> - 如果遇到断句标点 执行切句

代码：

```python
from automata import condition, operation
from automata.state_machine import StateMachine
from automata.sequence import StrSequence

# step 1: 初始所以需要的边和节点

edges = {
    'is_end_symbol': condition.IsEndSymbolCN(),
    'is_end_state': condition.IsEndState(),
}

nodes = {
    'init': operation.Indolent(),
    'do_cut': operation.Normal(),
    'end': operation.EndState()
}

# step 2: 构建图

simple_logic = {
    nodes['init']: [
        {'edge': edges['is_end_state'],
         'node': nodes['end']},

        {'edge': edges['is_end_symbol'],
         'node': nodes['do_cut']}
    ],
    nodes['do_cut']: [
        {'edge': edges['is_end_state'],
         'node': nodes['end']},

        {'edge': None,
         'node': nodes['init']}  # else 状态

    ],
}

# step 3: 初始化状态机
machine = StateMachine(simple_logic)

# step 4: 切句测试
sentences = '万壑树参天，千山响杜鹃。山中一夜雨，树杪百重泉。汉女输橦布，巴人讼芋田。文翁翻教授，不敢倚先贤。'

out = machine.run(StrSequence(sentences))

print('\n'.join(out.sentence_list()))
```



输出：

```bash
万壑树参天，千山响杜鹃。
山中一夜雨，树杪百重泉。
汉女输橦布，巴人讼芋田。
文翁翻教授，不敢倚先贤。
```



注意：

> - machine 是从 Indolent状态开始便利，遍历顺序从上倒下
> - 每个状态必须先有end_state条件否则报错

### 5.2. 自定义节点和边

- 节点要保证输入和输出都是 `sequece.StrSequence`就可以放在状态机中运行
- 边要保证输入是 `sequece.StrSequence`输出是`bool`就可以放在状态机中运行

这里不再做演示





 







