//
// /**
//  *
//  */
// $(function(){
// 	initDg1();
// 	initDg2();
// })
//
// function initDg1(){
// 	$("#dg1").datagrid({
// 		url:'/huafeng/getData/',
// 		toolbar:'#hjkToolBar',
// 		onClickRow:function(row){
// 			domDetail()
// 		},
// 		autoRowHeight:true,
// 		method:'post',
// 		columns:[[
// 		    {field:'collectNodeId', title:'采集节点编号', width:'8%',},
// 		    {field:'collectNodeName',title:'采集节点名称',width:'14%',},
// 		    {field:'collectNodeRegion',title:'采集节点所属区域',width:'14%',},
// 		    {field:'taskName',title:'采集任务',width:'14%',},
// 			{field:'taskStatus',title:'采集任务状态',width:'14%',formatter:function (v, r, i) {
//                 if(r.state == '1'){
//                     return '正在采集'
//                 } else if(r.state == '0'){
//                     return '未运行'
//                 }else if(r.state == '2'){
//                     return '采集出错'
//                 }else{
//                     return '未运行'
//                 }
//             }},
// 			{field:'allCount',title:'采集总数量',width:'14%',},
// 			{field:'successCount',title:'采集成功总数量',width:'14%',},
//             {field:'successRate',title:'成功率',width:'8%',},
// 		]],
//         onLoadSuccess:function(){
//         	console.log(1)
//         }
// 	})
// 	$('#search').searchbox({
//         prompt:'请输入地域名称',
//         height:24,
//         width:200,
//         searcher:function(v,n){
//            $('#dg1').datagrid('load', {condition:v})
//         }
//     })
// }
//
// function initDg2(){
// 	$("#dg2").datagrid({
// 		url:'/huafeng/getData1/',
// 		toolbar:'#bhkToolBar',
// 		autoRowHeight:true,
// 		singleSelect:true,
// 		method:'post',
// 		columns:[[
// 			{field:'fromtable',title:'数据来源表',width:'23%',},
// 			{field:'totable',title:'数据去向表',width:'22%',},
// 			{field:'datacounts',title:'数据总量',width:'15%',},
// 		    {field:'time',title:'清洗时间',width:'18%',},
// 		    {field:'successrate',title:'正常率',width:'23%',formatter:function(v,r,i){
// 				return formatterSuccessRate(r.successrate)
// 		    	//return (Number(r.successrate) * 100).toFixed(2) + '%';
// 			}},
// 		]],
// 	})
// 	$('#search2').searchbox({
//         prompt:'请输入来源库名称',
//         height:24,
//         width:200,
//         searcher:function(v,n){
//            $('#dg2').datagrid('load', {condition:v})
//         }
//     })
// }
//
//
// function formatterSuccessRate(rate){
// 	var res = Number(rate) * 100;
// 	if(res.toString().indexOf('.') != -1){
// 		return Number(res).toFixed(2) + '%'
// 	}else if(res != 0){
// 		return res + '%'
// 	}else{
// 		return res
// 	}
// }
//
// function initDg(tabIndex){
// 	switch (tabIndex){
// 	case 0:
// 		initDg1();
// 		break;
// 	case 1:
// 		initDg2();
// 		break;
// 	default:
// 		break;
// 	}
// }
//
// function domDetail() {
// 	var data = $("#dg1").datagrid('getSelected');
// 	data_cjdomid=data.cjdomid;
// 	console.log(data);
// 	console.log(data_cjdomid);
// 	$.get('/huafeng/biaozhunku_request/',{data:data_cjdomid},function(msg){
// 		window.open('/huafeng/secondPage/','_self')
// 		$("#dg1").datagrid('unselectAll')
// 	})
// }




