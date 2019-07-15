create database TD_LTE
on primary
(
   name='LTE_primary',
   filename='C:\db.TD-LTE\TD-LTE.primary.mdf'
),
filegroup LTE_filegroup_1
(
   name='LTE_fg1',
   filename='D:\db.TD-LTE\TD-LTE.fg1.ndf'
),
filegroup LTE_filegroup_2
(
   name='LTE_fg2',
   filename='E:\db.TD-LTE\TD-LTE.fg2.ndf'
),
filegroup LTE_filegroup_3
(
   name='LTE_fg3',
   filename='F:\db.TD-LTE\TD-LTE.fg3.ndf'
)
log on
(
   name='LTE_log',
   filename='C:\db.TD-LTE\TD-LTE.ldf'
)
go
alter database TD_LTE
modify filegroup LTE_filegroup_3 default
go

use TD_LTE
go

create table tbATUC2I (
   SECTOR_ID            nvarchar(50)         not null,
   NCELL_ID             nvarchar(50)         not null,
   RATIO_ALL            float                null,
   RANK                 int                  null,
   COSITE               tinyint              null
      check (COSITE is null or (COSITE in (0,1))),
   primary key (SECTOR_ID, NCELL_ID)
)
go

create table tbATUData (
   seq                  bigint               not null,
   FileName             nvarchar(255)        not null,
   Time                 varchar(100)         null,
   Longitude            float                null,
   Latitude             float                null,
   CellID               nvarchar(50)         null,
   TAC                  int                  null,
   EARFCN               int                  null,
   PCI                  smallint             null,
   RSRP                 float                null,
   RS_SINR              float                null,
   NCell_ID_1           nvarchar(50)         null,
   NCell_EARFCN_1       int                  null,
   NCell_PCI_1          smallint             null,
   NCell_RSRP_1         float                null,
   NCell_ID_2           nvarchar(50)         null,
   NCell_EARFCN_2       int                  null,
   NCell_PCI_2          smallint             null,
   NCell_RSRP_2         float                null,
   NCell_ID_3           nvarchar(50)         null,
   NCell_EARFCN_3       int                  null,
   NCell_PCI_3          smallint             null,
   NCell_RSRP_3         float                null,
   NCell_ID_4           nvarchar(50)         null,
   NCell_EARFCN_4       int                  null,
   NCell_PCI_4          smallint             null,
   NCell_RSRP_4         float                null,
   NCell_ID_5           nvarchar(50)         null,
   NCell_EARFCN_5       int                  null,
   NCell_PCI_5          smallint             null,
   NCell_RSRP_5         float                null,
   NCell_ID_6           nvarchar(50)         null,
   NCell_EARFCN_6       int                  null,
   NCell_PCI_6          smallint             null,
   NCell_RSRP_6         float                null,
   primary key(seq, FileName)
)
go

create table tbATUHandOver (
   SSECTOR_ID           nvarchar(50)         not null,
   NSECTOR_ID           varchar(50)          not null,
   HOATT                int                  null,
   primary key (SSECTOR_ID, NSECTOR_ID)
)
go

create table tbAdjCell (
   S_SECTOR_ID          nvarchar(50)         not null,
   N_SECTOR_ID          nvarchar(50)         not null,
   S_EARFCN             int                  null,
   N_EARFCN             int                  null,
   primary key (S_SECTOR_ID, N_SECTOR_ID)
)
go

create table tbC2I (
   CITY                 nvarchar(255)        null,
   SCELL                nvarchar(50)        not null,
   NCELL                nvarchar(50)        not null,
   PrC2I9               float                null,
   C2I_Mean             float                null,
   Std                  float                null,
   SampleCount          float                null,
   WeightedC2I          float                null,
   primary key (SCELL, NCELL)
)
go

create table tbCELL (
   CITY                 nvarchar(255)        null,
   SECTOR_ID            nvarchar(50)         not null,
   SECTOR_NAME          nvarchar(255)        not null,
   ENODEB_ID             int                  not null,
   ENODEB_NAME          nvarchar(255)        not null,
   EARFCN               int                  not null
      check (EARFCN in (37900,38098,38400,38496,38544,38950,39148)),
   PCI                  int                  null
      check (PCI is null or (PCI between 0 and 503)),
   PSS                  int                  null,
   SSS                  int                  null
      check (SSS is null or (SSS between 0 and 167)),
   TAC                  int                  null,
   VENDOR               nvarchar(255)        null
      check (VENDOR is null or (VENDOR in('华为','中兴','诺西','爱立信','贝尔','大唐'))),
   LONGITUDE            float                not null,
   LATITUDE             float                not null,
   STYLE                nvarchar(255)        null
      check (STYLE is null or (STYLE in('室分','宏站'))),
   AZIMUTH              float                not null,
   HEIGHT               float                null,
   ELECTTILT            float                null,
   MECHTILT             float                null,
   TOTLETILT            float                null,
   primary key (SECTOR_ID)
) on LTE_filegroup_1
create index CELL_IND1 on tbCELL (SECTOR_NAME)
create index CELL_IND2 on tbCELL (ENODEB_ID)
create index CELL_IND3 on tbCELL (ENODEB_NAME)
go

create trigger tri_insert_tbCELL
on tbCELL
instead of insert
as
begin 
delete from tbCELL where SECTOR_ID in(select SECTOR_ID from inserted)
insert into tbCEll select *from inserted
end
go

create table tbHandOver (
   CITY                 nvarchar(255)        null,
   SCELL                varchar(50)          not null,
   NCELL                varchar(50)          not null,
   HOATT                int                  null,
   HOSUCC               int                  null,
   HOSUCCRATE           float                null,
   primary key (SCELL, NCELL)
)
go

create table tbMROData (
   ID                   bigint               not null,
   TimeStamp            nvarchar(30)         not null,
   ServingSector        nvarchar(50)         not null,
   InterferingSector    nvarchar(50)         not null,
   LteScRSRP            float                null,
   LteNcRSRP            float                null,
   LteNcEarfcn          int                  null,
   LteNcPci             smallint             null,
   primary key nonclustered (id)
) on [primary]
create clustered index PK_MROData on tbMROData(TimeStamp,ServingSector,InterferingSector)
go

create trigger tri_insert_tbMROData
on tbMROData
instead of insert
as
begin 
	declare @a int
	declare
		@ID bigint,
		@TimeStamp nvarchar(30),
		@ServingSector nvarchar(50),
		@InterferingSector nvarchar(50),
		@LteScRSRP float,
		@LteNcRSRP float,
		@LteNcEarfcn int,
		@LteNcPci smallint
	declare cur cursor local forward_only for select * from inserted
	set @a= (select max(ID)+1 from tbMROData)
	if @a is null
		set @a=0
	open cur
	fetch next from cur into @ID,@TimeStamp,@ServingSector,@InterferingSector,@LteScRSRP,@LteNcRSRP,@LteNcEarfcn,@LteNcPci
	while @@fetch_status=0
	begin
		fetch next from cur into @ID,@TimeStamp,@ServingSector,@InterferingSector,@LteScRSRP,@LteNcRSRP,@LteNcEarfcn,@LteNcPci
		set @ID=@a
		set @a=@a+1
		insert into tbMROData values(@ID,@TimeStamp,@ServingSector,@InterferingSector,@LteScRSRP,@LteNcRSRP,@LteNcEarfcn,@LteNcPci)
	end
end
go

create table tbOptCell (
   SECTOR_ID            nvarchar(50)         not null,
   EARFCN               int                  null
      check (EARFCN is null or (EARFCN in (37900,38098,38400,38496,38544,38950,39148))),
   CELL_TYPE            nvarchar(50)         null
      check (CELL_TYPE is null or (CELL_TYPE in ('优化区','保护带'))),
   primary key (SECTOR_ID)
)
go

create table tbPCIAssignment (
   ASSIGN_ID            smallint             not null,
   EARFCN               int                  null
      check (EARFCN is null or (EARFCN in (37900,38098,38400,38496,38544,38950,39148))),
   SECTOR_ID            nvarchar(50)         null,
   SECTOR_NAME          nvarchar(200)        null,
   ENODEB_ID             int                  null,
   PCI                  int                  null
      check (PCI is null or (PCI between 0 and 503)),
   PSS                  int                  null,
   SSS                  int                  null
      check (SSS is null or (SSS between 0 and 167)),
   LONGITUDE            float                null
      check (LONGITUDE is null or (LONGITUDE between -180 and 180)),
   LATITUDE             float                null
      check (LATITUDE is null or (LATITUDE between -90 and 90)),
   STYLE                varchar(50)          null
      check (STYLE is null or (STYLE in ('室分','宏站'))),
   OPT_DATETIME         datetime             null,
   primary key (ASSIGN_ID)
)
go


create trigger tri_insert_tbPCIAss
on tbPCIAssignment
instead of insert
as
begin 
	declare @a int
	declare
		@ASSIGN_ID smallint,
		@EARFCN int,
		@SECTOR_ID nvarchar(50),
		@SECTOR_NAME nvarchar(200),
		@ENODEB_ID int,
		@PCI int,
		@PSS int,
		@SSS int,
		@LONGITUDE float,
		@LATITUDE float,
		@STYLE varchar(50),
		@OPT_DATETIME datetime
	declare cur cursor local forward_only for select * from inserted
	set @a= (select max(ASSIGN_ID)+1 from tbPCIAssignment)
	if @a is null
		set @a=0
	open cur
	fetch next from cur into @ASSIGN_ID,@EARFCN,@SECTOR_ID,@SECTOR_NAME,@ENODEB_ID,@PCI,@PSS,@SSS,@LONGITUDE,@LATITUDE,@STYLE,@OPT_DATETIME
	while @@fetch_status=0
	begin
		fetch next from cur into @ASSIGN_ID,@EARFCN,@SECTOR_ID,@SECTOR_NAME,@ENODEB_ID,@PCI,@PSS,@SSS,@LONGITUDE,@LATITUDE,@STYLE,@OPT_DATETIME
		set @ASSIGN_ID=@a
		set @a=@a+1
		insert into tbPCIAssignment values(@ASSIGN_ID,@EARFCN,@SECTOR_ID,@SECTOR_NAME,@ENODEB_ID,@PCI,@PSS,@SSS,@LONGITUDE,@LATITUDE,@STYLE,@OPT_DATETIME)
	end
end
go

create table tbSecAdjCell (
   SECTOR_ID            varchar(50)          not null,
   N_SECTOR_ID          varchar(50)          not null,
   primary key (SECTOR_ID, N_SECTOR_ID)
)
go

create table tbKPI(ENODEB_NAME
   STARTTIME            datetime             not null,
   ENODEB_NAME          nvarchar(255)        not null,
   SECTOR_NAME          nvarchar(255)        not null,
   REMARKS              nvarchar(255),
   RRC连接建立完成次数 int,                    
   RRC连接请求次数 int,
   RRC建立成功率 float,
   [E-RAB建立成功总次数] int,
   [E-RAB建立尝试总次数] int,
   [E-RAB建立成功率] float,
   [eNodeB触发的E-RAB异常释放总次数] int,
   [小区切换出E-RAB异常释放总次数] int,
   [E-RAB掉线率] float,
   无线接通率 float,
   eNodeB发起的S1RESET导致的UEContext释放次数 int,
   UEContext异常释放次数 int,
   UEContext建立成功总次数 int,
   无线掉线率 float,
   eNodeB内异频切换出成功次数 int,
   eNodeB内异频切换出尝试次数 int,
   eNodeB内同频切换出成功次数 int,
   eNodeB内同频切换出尝试次数 int,
   eNodeB间异频切换出成功次数 int,
   eNodeB间异频切换出尝试次数 int,
   eNodeB间同频切换出成功次数 int,
   eNodeB间同频切换出尝试次数 int,
   eNB内切换成功率 float,
   eNB间切换成功率 float,
   同频切换成功率zsp float,
   异频切换成功率zsp float,
   切换成功率 float,
   小区PDCP层所接收到的上行数据的总吞吐量 bigint,
   小区PDCP层所发送的下行数据的总吞吐量 bigint,
   RRC重建请求次数 int,
   RRC连接重建比率 float,
   通过重建回源小区的eNodeB间同频切换出执行成功次数 int,
   通过重建回源小区的eNodeB间异频切换出执行成功次数 int,
   通过重建回源小区的eNodeB内同频切换出执行成功次数 int,
   通过重建回源小区的eNodeB内异频切换出执行成功次数 int,
   eNB内切换出成功次数 int,
   eNB内切换出请求次数 int,
   primary key (STARTTIME, SECTOR_NAME)
)on LTE_filegroup_2
create nonclustered index ind_KPI on tbKPI(ENODEB_NAME)
go
create trigger tri_insert_tbKPI
on tbKPI
instead of insert
as
begin
   declare @STARTTIME datetime,@SECTOR_NAME nvarchar(255)
	declare cur cursor local forward_only for select STARTTIME, SECTOR_NAME from inserted
	open cur
	fetch next from cur into @STARTTIME,@SECTOR_NAME
	while @@fetch_status=0
	begin
		fetch next from cur into @STARTTIME,@SECTOR_NAME
      if exists(select * from tbKPI where STARTTIME=@STARTTIME and SECTOR_NAME=@SECTOR_NAME)
         delete from tbKPI where STARTTIME=@STARTTIME and SECTOR_NAME=@SECTOR_NAME
	end
   insert into tbKPI select * from inserted
end
go

create table tbPRB(
   STARTTIME            datetime             not null,
   ENODEB_NAME          nvarchar(255)        not null,
   SECTOR_NAME          nvarchar(255)        not null,
   REMARKS              nvarchar(255),
   AVG_0	int	null,
   AVG_1	int	null,
   AVG_2	int	null,
   AVG_3	int	null,
   AVG_4	int	null,
   AVG_5	int	null,
   AVG_6	int	null,
   AVG_7	int	null,
   AVG_8	int	null,
   AVG_9	int	null,
   AVG_10	int	null,
   AVG_11	int	null,
   AVG_12	int	null,
   AVG_13	int	null,
   AVG_14	int	null,
   AVG_15	int	null,
   AVG_16	int	null,
   AVG_17	int	null,
   AVG_18	int	null,
   AVG_19	int	null,
   AVG_20	int	null,
   AVG_21	int	null,
   AVG_22	int	null,
   AVG_23	int	null,
   AVG_24	int	null,
   AVG_25	int	null,
   AVG_26	int	null,
   AVG_27	int	null,
   AVG_28	int	null,
   AVG_29	int	null,
   AVG_30	int	null,
   AVG_31	int	null,
   AVG_32	int	null,
   AVG_33	int	null,
   AVG_34	int	null,
   AVG_35	int	null,
   AVG_36	int	null,
   AVG_37	int	null,
   AVG_38	int	null,
   AVG_39	int	null,
   AVG_40	int	null,
   AVG_41	int	null,
   AVG_42	int	null,
   AVG_43	int	null,
   AVG_44	int	null,
   AVG_45	int	null,
   AVG_46	int	null,
   AVG_47	int	null,
   AVG_48	int	null,
   AVG_49	int	null,
   AVG_50	int	null,
   AVG_51	int	null,
   AVG_52	int	null,
   AVG_53	int	null,
   AVG_54	int	null,
   AVG_55	int	null,
   AVG_56	int	null,
   AVG_57	int	null,
   AVG_58	int	null,
   AVG_59	int	null,
   AVG_60	int	null,
   AVG_61	int	null,
   AVG_62	int	null,
   AVG_63	int	null,
   AVG_64	int	null,
   AVG_65	int	null,
   AVG_66	int	null,
   AVG_67	int	null,
   AVG_68	int	null,
   AVG_69	int	null,
   AVG_70	int	null,
   AVG_71	int	null,
   AVG_72	int	null,
   AVG_73	int	null,
   AVG_74	int	null,
   AVG_75	int	null,
   AVG_76	int	null,
   AVG_77	int	null,
   AVG_78	int	null,
   AVG_79	int	null,
   AVG_80	int	null,
   AVG_81	int	null,
   AVG_82	int	null,
   AVG_83	int	null,
   AVG_84	int	null,
   AVG_85	int	null,
   AVG_86	int	null,
   AVG_87	int	null,
   AVG_88	int	null,
   AVG_89	int	null,
   AVG_90	int	null,
   AVG_91	int	null,
   AVG_92	int	null,
   AVG_93	int	null,
   AVG_94	int	null,
   AVG_95	int	null,
   AVG_96	int	null,
   AVG_97	int	null,
   AVG_98	int	null,
   AVG_99	int	null,
   primary key (STARTTIME,SECTOR_NAME)
)on [primary]
go
create nonclustered index ind_PRB on tbPRB(SECTOR_NAME,STARTTIME)
go
create trigger tri_insert_tbPRB
on tbPRB
instead of insert
as
begin
   declare @STARTTIME datetime,@SECTOR_NAME nvarchar(255)
	declare cur cursor local forward_only for select STARTTIME, SECTOR_NAME from inserted
	open cur
	fetch next from cur into @STARTTIME,@SECTOR_NAME
	while @@fetch_status=0
	begin
		fetch next from cur into @STARTTIME,@SECTOR_NAME
      if exists(select * from tbPRB where STARTTIME=@STARTTIME and SECTOR_NAME=@SECTOR_NAME)
         delete from tbPRB where STARTTIME=@STARTTIME and SECTOR_NAME=@SECTOR_NAME
	end
   insert into tbPRB select * from inserted
end
go

create table tbPRBnew(
   STARTTIME            datetime             not null,
   ENODEB_NAME          nvarchar(255)        not null,
   SECTOR_NAME          nvarchar(255)        not null,
   REMARKS              nvarchar(255),
   AVG_0	int	null,
   AVG_1	int	null,
   AVG_2	int	null,
   AVG_3	int	null,
   AVG_4	int	null,
   AVG_5	int	null,
   AVG_6	int	null,
   AVG_7	int	null,
   AVG_8	int	null,
   AVG_9	int	null,
   AVG_10	int	null,
   AVG_11	int	null,
   AVG_12	int	null,
   AVG_13	int	null,
   AVG_14	int	null,
   AVG_15	int	null,
   AVG_16	int	null,
   AVG_17	int	null,
   AVG_18	int	null,
   AVG_19	int	null,
   AVG_20	int	null,
   AVG_21	int	null,
   AVG_22	int	null,
   AVG_23	int	null,
   AVG_24	int	null,
   AVG_25	int	null,
   AVG_26	int	null,
   AVG_27	int	null,
   AVG_28	int	null,
   AVG_29	int	null,
   AVG_30	int	null,
   AVG_31	int	null,
   AVG_32	int	null,
   AVG_33	int	null,
   AVG_34	int	null,
   AVG_35	int	null,
   AVG_36	int	null,
   AVG_37	int	null,
   AVG_38	int	null,
   AVG_39	int	null,
   AVG_40	int	null,
   AVG_41	int	null,
   AVG_42	int	null,
   AVG_43	int	null,
   AVG_44	int	null,
   AVG_45	int	null,
   AVG_46	int	null,
   AVG_47	int	null,
   AVG_48	int	null,
   AVG_49	int	null,
   AVG_50	int	null,
   AVG_51	int	null,
   AVG_52	int	null,
   AVG_53	int	null,
   AVG_54	int	null,
   AVG_55	int	null,
   AVG_56	int	null,
   AVG_57	int	null,
   AVG_58	int	null,
   AVG_59	int	null,
   AVG_60	int	null,
   AVG_61	int	null,
   AVG_62	int	null,
   AVG_63	int	null,
   AVG_64	int	null,
   AVG_65	int	null,
   AVG_66	int	null,
   AVG_67	int	null,
   AVG_68	int	null,
   AVG_69	int	null,
   AVG_70	int	null,
   AVG_71	int	null,
   AVG_72	int	null,
   AVG_73	int	null,
   AVG_74	int	null,
   AVG_75	int	null,
   AVG_76	int	null,
   AVG_77	int	null,
   AVG_78	int	null,
   AVG_79	int	null,
   AVG_80	int	null,
   AVG_81	int	null,
   AVG_82	int	null,
   AVG_83	int	null,
   AVG_84	int	null,
   AVG_85	int	null,
   AVG_86	int	null,
   AVG_87	int	null,
   AVG_88	int	null,
   AVG_89	int	null,
   AVG_90	int	null,
   AVG_91	int	null,
   AVG_92	int	null,
   AVG_93	int	null,
   AVG_94	int	null,
   AVG_95	int	null,
   AVG_96	int	null,
   AVG_97	int	null,
   AVG_98	int	null,
   AVG_99	int	null,
   primary key (STARTTIME,SECTOR_NAME)
)on [primary]
go
create nonclustered index ind on tbKPI(ENODEB_NAME,STARTTIME)
go

create table tbC2Inew(
   SCELL                nvarchar(50)        not null,
   NCELL                nvarchar(50)        not null,
   C2I_Mean             float                null,
   Std                  float                null,
   PrbC2I9              float                null,
   PrbABS6              float                null,
   primary key (SCELL, NCELL)
)on LTE_filegroup_1
go

create table tbC2I3(
   CELL1                nvarchar(50)        not null,
   CELL2                nvarchar(50)        not null,
   CELL3                nvarchar(50)        not null,
   primary key (CELL1, CELL2, CELL3)
)on LTE_filegroup_2
go

create procedure C2I_Analyse @minimum int
as
begin
	insert into tbC2Inew
	   select ServingSector,InterferingSector,avg(C2I) as C2I_mean,stdev(C2I) as Std,null as PrbC2I9,null as PrbABS6
	   from(
   			select ServingSector,InterferingSector,(LteScRSRP-LteNcRSRP)as C2I 
   			from tbMROData as t
   			where (ServingSector+'to'+InterferingSector) in(
				select ServingSector+'to'+InterferingSector as sectors
				from tbMROData as b
				group by ServingSector,InterferingSector 
				having count(*)>=@minimum
			)
		) as a
	   group by ServingSector,InterferingSector
end
go

create procedure hourly_PRB
as
begin
	insert into tbPRBnew 
	select b.STARTTIME_HOUR,ENODEB_NAME,b.SECTOR_NAME,REMARKS,
		b.AVG_0,b.AVG_1,b.AVG_2,b.AVG_3,b.AVG_4,b.AVG_5,b.AVG_6,b.AVG_7,b.AVG_8,b.AVG_9,
		b.AVG_10,b.AVG_11,b.AVG_12,b.AVG_13,b.AVG_14,b.AVG_15,b.AVG_16,b.AVG_17,b.AVG_18,b.AVG_19,
		b.AVG_20,b.AVG_21,b.AVG_22,b.AVG_23,b.AVG_24,b.AVG_25,b.AVG_26,b.AVG_27,b.AVG_28,b.AVG_29,
		b.AVG_30,b.AVG_31,b.AVG_32,b.AVG_33,b.AVG_34,b.AVG_35,b.AVG_36,b.AVG_37,b.AVG_38,b.AVG_39,
		b.AVG_40,b.AVG_41,b.AVG_42,b.AVG_43,b.AVG_44,b.AVG_45,b.AVG_46,b.AVG_47,b.AVG_48,b.AVG_49,
		b.AVG_50,b.AVG_51,b.AVG_52,b.AVG_53,b.AVG_54,b.AVG_55,b.AVG_56,b.AVG_57,b.AVG_58,b.AVG_59,
		b.AVG_60,b.AVG_61,b.AVG_62,b.AVG_63,b.AVG_64,b.AVG_65,b.AVG_66,b.AVG_67,b.AVG_68,b.AVG_69,
		b.AVG_70,b.AVG_71,b.AVG_72,b.AVG_73,b.AVG_74,b.AVG_75,b.AVG_76,b.AVG_77,b.AVG_78,b.AVG_79,
		b.AVG_80,b.AVG_81,b.AVG_82,b.AVG_83,b.AVG_84,b.AVG_85,b.AVG_86,b.AVG_87,b.AVG_88,b.AVG_89,
		b.AVG_90,b.AVG_91,b.AVG_92,b.AVG_93,b.AVG_94,b.AVG_95,b.AVG_96,b.AVG_97,b.AVG_98,b.AVG_99
	from(
			select (left(STARTTIME,13)+':00:00')as STARTTIME_HOUR,SECTOR_NAME,
				avg(AVG_0)as AVG_0,avg(AVG_1)as AVG_1,avg(AVG_2)as AVG_2,avg(AVG_3)as AVG_3,avg(AVG_4)as AVG_4,
				avg(AVG_5)as AVG_5,avg(AVG_6)as AVG_6,avg(AVG_7)as AVG_7,avg(AVG_8)as AVG_8,avg(AVG_9)as AVG_9,
				avg(AVG_10)as AVG_10,avg(AVG_11)as AVG_11,avg(AVG_12)as AVG_12,avg(AVG_13)as AVG_13,avg(AVG_14)as AVG_14,
				avg(AVG_15)as AVG_15,avg(AVG_16)as AVG_16,avg(AVG_17)as AVG_17,avg(AVG_18)as AVG_18,avg(AVG_19)as AVG_19,
				avg(AVG_20)as AVG_20,avg(AVG_21)as AVG_21,avg(AVG_22)as AVG_22,avg(AVG_23)as AVG_23,avg(AVG_24)as AVG_24,
				avg(AVG_25)as AVG_25,avg(AVG_26)as AVG_26,avg(AVG_27)as AVG_27,avg(AVG_28)as AVG_28,avg(AVG_29)as AVG_29,
				avg(AVG_30)as AVG_30,avg(AVG_31)as AVG_31,avg(AVG_32)as AVG_32,avg(AVG_33)as AVG_33,avg(AVG_34)as AVG_34,
				avg(AVG_35)as AVG_35,avg(AVG_36)as AVG_36,avg(AVG_37)as AVG_37,avg(AVG_38)as AVG_38,avg(AVG_39)as AVG_39,
				avg(AVG_40)as AVG_40,avg(AVG_41)as AVG_41,avg(AVG_42)as AVG_42,avg(AVG_43)as AVG_43,avg(AVG_44)as AVG_44,
				avg(AVG_45)as AVG_45,avg(AVG_46)as AVG_46,avg(AVG_47)as AVG_47,avg(AVG_48)as AVG_48,avg(AVG_49)as AVG_49,
				avg(AVG_50)as AVG_50,avg(AVG_51)as AVG_51,avg(AVG_52)as AVG_52,avg(AVG_53)as AVG_53,avg(AVG_54)as AVG_54,
				avg(AVG_55)as AVG_55,avg(AVG_56)as AVG_56,avg(AVG_57)as AVG_57,avg(AVG_58)as AVG_58,avg(AVG_59)as AVG_59,
				avg(AVG_60)as AVG_60,avg(AVG_61)as AVG_61,avg(AVG_62)as AVG_62,avg(AVG_63)as AVG_63,avg(AVG_64)as AVG_64,
				avg(AVG_65)as AVG_65,avg(AVG_66)as AVG_66,avg(AVG_67)as AVG_67,avg(AVG_68)as AVG_68,avg(AVG_69)as AVG_69,
				avg(AVG_70)as AVG_70,avg(AVG_71)as AVG_71,avg(AVG_72)as AVG_72,avg(AVG_73)as AVG_73,avg(AVG_74)as AVG_74,
				avg(AVG_75)as AVG_75,avg(AVG_76)as AVG_76,avg(AVG_77)as AVG_77,avg(AVG_78)as AVG_78,avg(AVG_79)as AVG_79,
				avg(AVG_80)as AVG_80,avg(AVG_81)as AVG_81,avg(AVG_82)as AVG_82,avg(AVG_83)as AVG_83,avg(AVG_84)as AVG_84,
				avg(AVG_85)as AVG_85,avg(AVG_86)as AVG_86,avg(AVG_87)as AVG_87,avg(AVG_88)as AVG_88,avg(AVG_89)as AVG_89,
				avg(AVG_90)as AVG_90,avg(AVG_91)as AVG_91,avg(AVG_92)as AVG_92,avg(AVG_93)as AVG_93,avg(AVG_94)as AVG_94,
				avg(AVG_95)as AVG_95,avg(AVG_96)as AVG_96,avg(AVG_97)as AVG_97,avg(AVG_98)as AVG_98,avg(AVG_99)as AVG_99
			from tbPRB
			group by left(STARTTIME,13),SECTOR_NAME
		) as b,tbPRB
      where b.STARTTIME_HOUR=tbPRB.STARTTIME and b.SECTOR_NAME=tbPRB.SECTOR_NAME
	end
go

create procedure generate_triSector @rate float
as
	begin
		with bisector as(
			select SCELL,NCELL
			from tbC2Inew
			where PrbABS6>@rate
			union
			select NCELL,SCELL
			from tbC2Inew
			where PrbABS6>@rate
		)
      insert into tbC2I3
   		select distinct a.SCELL,a.NCELL,b.SCELL
	   	from bisector as a,bisector as b
		   where a.SCELL=b.NCELL and a.SCELL<>b.SCELL and a.SCELL>a.NCELL and a.NCELL>b.SCELL
	end
go