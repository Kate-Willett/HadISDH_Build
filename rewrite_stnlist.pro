pro rewrite_stnlist

spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317q/meta/7317q_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317e/meta/7317e_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317rh/meta/7317rh_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317t/meta/7317t_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317td/meta/7317td_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317tw/meta/7317tw_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317dpd/meta/7317dpd_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317slp/meta/7317slp_metadata_file.txt'
spawn,'touch ''../PHA2015/pha52jgo/data/hadisdh/7317ws/meta/7317ws_metadata_file.txt'


openr,5,'../../LISTS_DOCS/goodforHadISDH.3.0.1.2017p_JAN2018.txt'
openw,10,'../PHA2015/pha52jgo/data/hadisdh/7317q/meta/7317q_stnlist.tavg'
openw,11,'../PHA2015/pha52jgo/data/hadisdh/7317e/meta/7317e_stnlist.tavg'
openw,12,'../PHA2015/pha52jgo/data/hadisdh/7317rh/meta/7317rh_stnlist.tavg'
openw,13,'../PHA2015/pha52jgo/data/hadisdh/7317t/meta/7317t_stnlist.tavg'
openw,14,'../PHA2015/pha52jgo/data/hadisdh/7317td/meta/7317td_stnlist.tavg'
openw,15,'../PHA2015/pha52jgo/data/hadisdh/7317tw/meta/7317tw_stnlist.tavg'
openw,16,'../PHA2015/pha52jgo/data/hadisdh/7317dpd/meta/7317dpd_stnlist.tavg'
openw,17,'../PHA2015/pha52jgo/data/hadisdh/7317slp/meta/7317slp_stnlist.tavg'
openw,18,'../PHA2015/pha52jgo/data/hadisdh/7317ws/meta/7317ws_stnlist.tavg'
while not eof(5) do begin
  inid=''
  inlat=0.
  inlon=0.
  inelev=0.
  incid=''
  innamoo=''
  mush='' 
  readf,5,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f8.4,f10.4,f7.1,x,a2,x,a29,13x)'
  printf,10,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,11,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,12,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,13,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,14,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,15,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,16,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,17,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
  printf,18,inid,inlat,inlon,inelev,incid,innamoo,format='(a11,f7.2,f10.2,8x,i5,x,a2,x,a29)'
endwhile
close,5
close,10


end
