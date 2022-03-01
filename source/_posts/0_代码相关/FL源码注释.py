# 训练文件 京东是leader
python -m fedlearner.model.tree.trainer leader \
    --local-addr=localhost:50051 \
    --peer-addr=localhost:50052 \
    --data-path=data/leader_train.csv \
    --export-model-path=leader_model.proto \
    --verify-example-ids=true

# booster
fedlearner.model.tree.tree.BoostingTreeEnsamble #batch 打分之类的
·····_fit_one_round_local  _fit_one_round_leader  _fit_one_round_follower 

BaseGrower()
   self._compute_histogram(self._nodes[0])
   self._find_split_and_push(self._nodes[0])


LeaderGrower().grow() #节点分裂等主脚本
FollowerGrower()
  _compute_histogram()
  _split_next


# 通信模块,定义端口，channel，地址等
bridge = fedlearner.trainer.bridge.Bridge(args.role, int(args.local_addr.split(':')[1]),
                        args.peer_addr, args.application_id, 0,
                        streaming_mode=args.use_streaming)
# Bridge模块方法
msg = tws_pb.TrainerWorkerMessage(commit=tws_pb.CommitMessage(
            iter_id=last_iter_id))
msg = tws_pb.LoadDataBlockRequest(count=count, block_id=block_id)
        return self._client.LoadDataBlock(msg)

#定义模型
booster = fedlearner.model.tree.tree.BoostingTreeEnsamble(
            bridge,
            learning_rate=args.learning_rate,
            max_iters=args.max_iters,
            max_depth=args.max_depth,
            l2_regularization=args.l2_regularization,
            max_bins=args.max_bins,
            num_parallel=args.num_parallel)
booster.load_saved_model(args.load_model_path)
X, y, example_ids = read_csv_data(  # X, y:matrix   example_ids:list
        args.data_path, args.verify_example_ids,
        args.role != 'follower')
booster.fit(
        X, y,
        checkpoint_path=args.checkpoint_path,
        example_ids=example_ids,
        validation_features=val_X,
        validation_labels=val_y,
        validation_example_ids=val_example_ids,
        output_path=args.output_path)
	binned = BinnedFeatures(features, self._max_bins) #m*n 每个样本每个特征的分位点  features=X
	sum_prediction = self.batch_predict(features, get_raw_score=True) #weight之和 list length=样本数
	tree, raw_prediction = self._fit_one_round_leader(
                    sum_prediction, binned, labels)  #返回 grower.to_proto(), grower.get_prediction()
	
	tree = self._fit_one_round_follower(binned) #follower的侧训练

		# compute grad and hess 接收
        self._bridge.start(self._bridge.new_iter_id())
        grad = np.asarray(_receive_encrypted_numbers( #加密后的梯度  加密函数 _receive_encrypted_numbers
            self._bridge, 'grad', self._public_key))
        assert len(grad) == binned.features.shape[0]
        hess = np.asarray(_receive_encrypted_numbers(
            self._bridge, 'hess', self._public_key))
        assert len(hess) == binned.features.shape[0]
        self._bridge.commit()
        logging.info(
            'Follower starting iteration %d.',
            len(self._trees))

        grower = fedlearner.model.tree.tree.FollowerGrower(
            self._bridge, self._public_key,
            binned, grad, hess,
            learning_rate=self._learning_rate,
            max_depth=self._max_depth,
            max_leaves=self._max_leaves,
            l2_regularization=self._l2_regularization,
            grow_policy=self._grow_policy,
            num_parallel=self._num_parallel,
            pool=self._pool)

        grower.grow()
        # grow详细内容如下
        	#self._nodes = [GrowerNode(0)]  即node id 初始化为0
        	#计算该node上不同特征分箱上的梯度
        	self._compute_histogram(self._nodes[0])  #follower的分箱加密梯度和通过 brideg.send_proto传回leader
			    def _compute_histogram(self, node):
			        self._bridge.start(self._bridge.new_iter_id())
			        grad_hists = self._hist_builder.compute_histogram(
			            self._grad, node.sample_ids)
			        hess_hists = self._hist_builder.compute_histogram(
			            self._hess, node.sample_ids)
			        self._send_histograms('grad_hists', grad_hists) 
			        self._send_histograms('hess_hists', hess_hists)
			        self._bridge.commit()

	        # leader方通过tree_pb2（tf serving）访问不同特征上的的
	        self._find_split_and_push(self._nodes[0])  #leader 的 _find_split_and_push  #follower的split和pass是pass
	            def _find_split_and_push(self, node):
			        split_info = tree_pb2.SplitInfo(
			            node_id=node.node_id, gain=-1)
			        for fid, (grad_hist, hess_hist) in enumerate(zip(node.grad_hists, node.hess_hists)): #fid表示特征分箱后的索引，10个特征5个分箱的话fid就是1-50
			            sum_g = sum(grad_hist)
			            sum_h = sum(hess_hist)
			            left_g = 0.0
			            left_h = 0.0
			            nan_g = grad_hist[-1]
			            nan_h = hess_hist[-1]
			            for i in range(len(grad_hist) - 2):
			                left_g += grad_hist[i]
			                left_h += hess_hist[i]
			                self._compare_split(
			                    split_info, True, fid, i,
			                    left_g + nan_g, left_h + nan_h,
			                    sum_g - left_g - nan_g, sum_h - left_h - nan_h)
			                self._compare_split(
			                    split_info, False, fid, i,
			                    left_g, left_h,
			                    sum_g - left_g, sum_h - left_h)

			        self._split_candidates.put((-split_info.gain, split_info))

			        return split_info.gain, split_info


	        while self._num_leaves < self._max_leaves:
	            left_child, right_child, split_info = self._split_next()
	            self._log_split(left_child, right_child, split_info)
	            self._compute_histogram(left_child)
	            self._find_split_and_push(left_child)
	            self._compute_histogram_from_sibling(right_child, left_child)
	            self._find_split_and_push(right_child)
	    
	    tree=grower.to_proto()





booster.save_model(args.export_path)

bridge.terminate()