$(function(){
	$("#mylist3").datagrid({
		url: "/huafeng/table_table/",
		method:'post',
		toolbar:'#toolbar',
		/*onClickRow:function(row){
			domDetail()
		},
		onDblClickRow:function(row){
			domDetail()
		},*/
		columns:[[
			{field:'resourceid',title:'id',width:'15%',align:'left',hidden:'true'},
			{field:'resourcename',title:'目录或资源名称',width:'55%',align:'left'},
			{field:'releasetime',title:'发布时间',width:'30%',align:'center'},
			{field:'typeid',title:'目录级别',width:'25%',align:'center',hidden:'true'},
			{field:'oper',title:'操作',width:'15%',formatter:operationDetail}
        ]],
		onLoadSuccess:function(){
			$('.detail').linkbutton({iconCls:'icon-more'})
		}
	})
	$('#search').searchbox({
        prompt:'请输入目录或资源名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist3').datagrid('load', {condition:v})
        }
    })
})

function operationDetail(value, row, index){
	return '<a class="detail" onclick="showDetail('+row.resourceid+')">详情</a>'
}

function showDetail(id){
	$('#tableDetailDialog').dialog({
		title:'资源详情',
		onOpen:function(){
			$('#ResourceAttr').propertygrid({
				fit:true,
				method:'post',
				showHeader:false,
				columns:[[
					{field:'name',width:'50%',showTitle:true,styler:function(value,row,index){
						return 'background-color:#E0ECFF';
					}},
					{field:'value',showTitle:true, width:'50%',},
				]],
				queryParams:{
					resourceid:id,
				},
				onClickRow:function(index, row){
					$(this).propertygrid('unSelect', index)
				}
			})
			$('#ResourceFieldList').datagrid({
				method:'post',
				columns:[[
					{field:'field_chinese',title:'资源中文名',width:'20%',showTitle:true,},
					{field:'field_english',title:'字段英文名',showTitle:true, width:'20%',},
					{field:'show_type',title:'字段类型',showTitle:true, width:'20%',},
					{field:'field_length',title:'字段长度',showTitle:true, width:'20%',},
					{field:'element_identifier',title:'数据元标识符',showTitle:true, width:'20%',},
				]],
				queryParams:{
					resourceid:id,
				},
				onClickRow:function(index, row){
					$(this).datagrid('unSelect', index)
				}
			})
		}
	}).dialog('open')
}



/*
function domDetail() {
	var data = $("#mylist3").datagrid('getSelected');
	data_resourceid=data.resourceid;
	data_resourcename=data.resourcename;
	console.log(data);
	console.log(data_resourceid);
	$.get('/huafeng/detailed_request/',{data1:data_resourceid,data2:data_resourcename,},function(msg){
		window.open('/huafeng/detailed/','_self')
		$("#mylist3").datagrid('unselectAll')
	})
}*/