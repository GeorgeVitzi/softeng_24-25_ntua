se2402 healthcheck
se2402 resetpasses
se2402 healthcheck
se2402 resetstations
se2402 healthcheck
se2402 admin --addpasses --source passes02.csv
se2402 healthcheck
se2402 tollstationpasses --station AM08 --from 20220213 --to 20220227 --format json
se2402 tollstationpasses --station NAO04 --from 20220213 --to 20220227 --format csv
se2402 tollstationpasses --station NO01 --from 20220213 --to 20220227 --format csv
se2402 tollstationpasses --station OO03 --from 20220213 --to 20220227 --format csv
se2402 tollstationpasses --station XXX --from 20220213 --to 20220227 --format csv
se2402 tollstationpasses --station OO03 --from 20220213 --to 20220227 --format YYY
se2402 errorparam --station OO03 --from 20220213 --to 20220227 --format csv
se2402 tollstationpasses --station AM08 --from 20220214 --to 20220225 --format json
se2402 tollstationpasses --station NAO04 --from 20220214 --to 20220225 --format csv
se2402 tollstationpasses --station NO01 --from 20220214 --to 20220225 --format csv
se2402 tollstationpasses --station OO03 --from 20220214 --to 20220225 --format csv
se2402 tollstationpasses --station XXX --from 20220214 --to 20220225 --format csv
se2402 tollstationpasses --station OO03 --from 20220214 --to 20220225 --format YYY
se2402 passanalysis --stationop AM --tagop NAO --from 20220213 --to 20220227 --format json
se2402 passanalysis --stationop NAO --tagop AM --from 20220213 --to 20220227 --format csv
se2402 passanalysis --stationop NO --tagop OO --from 20220213 --to 20220227 --format csv
se2402 passanalysis --stationop OO --tagop KO --from 20220213 --to 20220227 --format csv
se2402 passanalysis --stationop XXX --tagop KO --from 20220213 --to 20220227 --format csv
se2402 passanalysis --stationop AM --tagop NAO --from 20220214 --to 20220225 --format json
se2402 passanalysis --stationop NAO --tagop AM --from 20220214 --to 20220225 --format csv
se2402 passanalysis --stationop NO --tagop OO --from 20220214 --to 20220225 --format csv
se2402 passanalysis --stationop OO --tagop KO --from 20220214 --to 20220225 --format csv
se2402 passanalysis --stationop XXX --tagop KO --from 20220214 --to 20220225 --format csv
se2402 passescost --stationop AM --tagop NAO --from 20220213 --to 20220227 --format json
se2402 passescost --stationop NAO --tagop AM --from 20220213 --to 20220227 --format csv
se2402 passescost --stationop NO --tagop OO --from 20220213 --to 20220227 --format csv
se2402 passescost --stationop OO --tagop KO --from 20220213 --to 20220227 --format csv
se2402 passescost --stationop XXX --tagop KO --from 20220213 --to 20220227 --format csv
se2402 passescost --stationop AM --tagop NAO --from 20220214 --to 20220225 --format json
se2402 passescost --stationop NAO --tagop AM --from 20220214 --to 20220225 --format csv
se2402 passescost --stationop NO --tagop OO --from 20220214 --to 20220225 --format csv
se2402 passescost --stationop OO --tagop KO --from 20220214 --to 20220225 --format csv
se2402 passescost --stationop XXX --tagop KO --from 20220214 --to 20220225 --format csv
se2402 chargesby --opid NAO --from 20220213 --to 20220227 --format json
se2402 chargesby --opid GE --from 20220213 --to 20220227 --format csv
se2402 chargesby --opid OO --from 20220213 --to 20220227 --format csv
se2402 chargesby --opid KO --from 20220213 --to 20220227 --format csv
se2402 chargesby --opid NO --from 20220213 --to 20220227 --format csv
se2402 chargesby --opid NAO --from 20220214 --to 20220225 --format json
se2402 chargesby --opid GE --from 20220214 --to 20220225 --format csv
se2402 chargesby --opid OO --from 20220214 --to 20220225 --format csv
se2402 chargesby --opid KO --from 20220214 --to 20220225 --format csv
se2402 chargesby --opid NO --from 20220214 --to 20220225 --format csv
