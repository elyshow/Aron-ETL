$(function(){
	$("#journallist").datagrid({
		url: "/huafeng/journal_tablelog/",
		method:'post',
		toolbar:'#toolbar',
		singleSelect:true,
		fit:true,
		columns:[[
		    {field:'id',title:'id',align:'left',hidden:true},
			{field:'username',title:'用户名',width:'11%',align:'left'},
			{field:'apiID',title:'接口编号',width:'11%',align:'left'},
			{field:'data',title:'请求访问接口数据',width:'14%',align:'left'},
			{field:'requesttime',title:'请求时间',width:'18%',align:'left'},
			{field:'returnvalue',title:'返回接口数据',width:'14%',align:'left'},
			{field:'returntime',title:'返回时间',width:'18%',align:'left'},
			{field:'opear',title:'操作',width:'16%',align:'left',formatter:func},
        ]],
        
        onLoadSuccess:function(){
        	$('.stateDetail').linkbutton({
				iconCls: 'icon-more'
			});
	}
	})
	
	$('#search').searchbox({
        prompt:'请输入接口目录名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#journallist').datagrid('load', {condition:v})
        }
    })
})


function func() {
		return 	'<a class="stateDetail" href="javascript:detailTask();" data-options="" >数据详情</a>'
}

function detailTask(){
	linkbutton_click('open_dialog', {dialog: '#journal_dialog'});
	var list =''
	list = $('#journallist').datagrid('getSelections')
	var id = list[0].id
	
	 $.get('/huafeng/journal_dialog/', {datas:id}, function (yeat){
		 console.log(yeat[0]);
		 $("#username").val(yeat[0].username);
		 $("#apiID").val(yeat[0].apiID);
		 $("#data").val(yeat[0].data);
		 $("#requesttime").val(yeat[0].requesttime);
		 $("#returnvalue").val(yeat[0].returnvalue);
		 $("#returntime").val(yeat[0].returntime);
	 })
}
