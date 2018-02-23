$(function(){
	$("#mylist1").datagrid({
		url: "/huafeng/interfacecatalogue1_table/",
		method:'post',
		toolbar:'#toolbar',
		singleSelect:true,
		onClickRow:function(row){
			domDetail()
		},
		onDblClickRow:function(row){
			domDetail()
		},
		columns:[[
            {field:'cataloguename',title:'接口目录名称',width:'60%',align:'left'},
            {field:'typetime',title:'建立时间',width:'30%',align:'center'},
            {field:'count',title:'接口数量',width:'10%',align:'center'},
            {field:'typeid',title:'目录编号',width:'0%',align:'center',hidden:'true'},
        ]],
	})
	
	$('#search').searchbox({
        prompt:'请输入接口目录名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist1').datagrid('load', {condition:v})
        }
    })
})



function domDetail() {
	var data = $("#mylist1").datagrid('getSelected');
	data_typeid=data.typeid;
	$.get('/huafeng/interfacecatalogue2_request/',{data:data_typeid},function(msg){
		window.open('/huafeng/interfacecatalogue2/','_self')
		$("#mylist1").datagrid('unselectAll')
	})
}