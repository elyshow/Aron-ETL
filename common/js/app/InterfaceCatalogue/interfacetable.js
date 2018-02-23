$(function(){
	$("#mylist3").datagrid({
		url: "/huafeng/interfacetable_table/",
		method:'post',
		singleSelect:true,
		toolbar:'#toolbar',
		columns:[[
			{field:'idapi',title:'接口编号',width:'12%',align:'left'},
			{field:'nameapi',title:'接口名称',width:'16%',align:'left'},
			{field:'warehouseapi',title:'接口来源库',width:'11%',align:'left'},
			{field:'tableapi',title:'接口数据表',width:'11%',align:'left'},
			{field:'createtime',title:'注册时间',width:'15%',align:'left'},
			{field:'oper',title:'查看详情',width:'34%',align:'center',formatter:func},
        ]],	
        onLoadSuccess:function(){
			$('.detailMore').linkbutton({
				iconCls: 'icon-more',
			});
			$('.detailZiduan').linkbutton({
				iconCls: 'icon-search',
			});
	}
	})
	$('#search').searchbox({
        prompt:'请输入接口名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist1').datagrid('load', {condition:v})
        }
    })
})

function func(v,r,i){
	return  '<a class="easyui-linkbutton detailZiduan" href="javascript:domDetail();" data-option="" style="margin:0px 6px;">查看接口返回字段</a>'+
	        '<a class="easyui-linkbutton detailMore" href="javascript:conditionDetail();" data-option="" style="margin:0px 6px;">查看查询条件</a>'
}

function conditionDetail() {
	var data = $("#mylist3").datagrid('getSelected');
	data_idAPI=data.idapi;
	$.get('/huafeng/condition_request/',{data:data_idAPI},function(msg){
		window.open('/huafeng/condition/','_self')
		$("#mylist3").datagrid('unselectAll')
	})
}

function domDetail() {
	var data = $("#mylist3").datagrid('getSelected');
	data_idAPI=data.idapi;
	$.get('/huafeng/interfacedetailed_request/',{data:data_idAPI},function(msg){
		window.open('/huafeng/interfacedetailed/','_self')
		$("#mylist3").datagrid('unselectAll')
	})
}
