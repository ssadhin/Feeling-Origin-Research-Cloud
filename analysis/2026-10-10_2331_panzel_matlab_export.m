function export_panzel_baseline(behavioral_path, neural_path, output_csv)
% Schema-only, fail-closed converter for the frozen Panzel LOPO test.
% Run in MATLAB with original GitHub .mat files; NOT yet executed or validated.
B0=load(behavioral_path,'behavioral_baseline');
N0=load(neural_path,'neural_baseline');
assert(isfield(B0,'behavioral_baseline') && istable(B0.behavioral_baseline),'Missing MATLAB behavioral table');
assert(isfield(N0,'neural_baseline') && istable(N0.neural_baseline),'Missing MATLAB neural table');
B=B0.behavioral_baseline; N=N0.neural_baseline;
reqB={'ID','Group','Modality','Intensity','Rating'};
reqN={'subID','group','measure','modality','intensity','value'};
assert(all(ismember(reqB,B.Properties.VariableNames)),'Behavioral schema mismatch');
assert(all(ismember(reqN,N.Properties.VariableNames)),'Neural schema mismatch');
B=B(strcmpi(string(B.Modality),'Sound'),reqB);
N=N(strcmpi(string(N.modality),'Sound'),reqN);
B.ID=string(B.ID); N.subID=string(N.subID);
B.Intensity=string(B.Intensity); N.intensity=string(N.intensity);
B.Group=string(B.Group); N.group=string(N.group);
assert(all(ismember(B.Intensity,["Low","High"])),'Behavioral intensity labels invalid');
assert(all(ismember(N.intensity,["Low","High"])),'Neural intensity labels invalid');
bkeys=strcat(B.ID,'|',B.Intensity);
assert(numel(unique(bkeys))==height(B),'Duplicate behavioral ID/intensity');
A=N(strcmp(string(N.measure),'A1'),{'subID','intensity','value','group'});
G=N(strcmp(string(N.measure),'general'),{'subID','intensity','value','group'});
assert(~isempty(A) && ~isempty(G),'Missing A1 or general pattern');
A.Properties.VariableNames={'ID','Intensity','A1','NeuralGroupA1'};
G.Properties.VariableNames={'ID','Intensity','general','NeuralGroupGeneral'};
assert(numel(unique(strcat(A.ID,'|',A.Intensity)))==height(A),'Duplicate A1 ID/intensity');
assert(numel(unique(strcat(G.ID,'|',G.Intensity)))==height(G),'Duplicate general ID/intensity');
T=innerjoin(innerjoin(B,A,'Keys',{'ID','Intensity'}),G,'Keys',{'ID','Intensity'});
assert(height(T)>0,'No matched participant rows');
assert(all(strcmpi(T.NeuralGroupA1,T.NeuralGroupGeneral)),'Neural group disagreement');
assert(all((strcmpi(T.Group,'Healthy') & strcmpi(T.NeuralGroupA1,'HC')) | ...
           (strcmpi(T.Group,'CBP') & strcmpi(T.NeuralGroupA1,'CBP'))),'Behavior-neural group disagreement');
assert(numel(unique(strcat(T.ID,'|',T.Intensity)))==height(T),'Duplicate merged keys');
fprintf('Behavioral sound rows: %d; A1: %d; general: %d; matched: %d; distinct subjects: %d\n',...
 height(B),height(A),height(G),height(T),numel(unique(T.ID)));
T=T(:,{'ID','Group','Intensity','Rating','A1','general'});
writetable(T,output_csv);
fprintf('Exported %s. Do not infer phenomenality or causal mechanism from this table.\n',output_csv);
end
