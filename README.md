# ipmininet kvm


- Host Machine: namespace
- Interconnect: ipmininet


- ipmininet: Fat-treeの構築にはルータが必要であるが，mininetにはaddRouterメソッドがない．addRouterが用意されているipmininetを利用する
- namespace: MPIを実行する計算ノードとして利用する．Dockerとは異なり計算ノード内で複数プロセスを動作させる場合でも，namespaceであればプロセス数に特に制限はない．