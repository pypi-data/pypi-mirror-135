function  GEBI(x){return document.getElementById(x)}
function dumps(x){return JSON.stringify(x)}
function expose(contract, methods){
    function exposeCallMethod(c, f) {
	c[f] = function(){
	    return c.methods[f].apply(null, arguments).call({
		from: app.currentAccount})}}
    function exposeTransactMethod(c, f) {
	c[f] = function(){
	    return web3.eth.sendTransaction(
		{from: app.currentAccount,
		 to  : c.options.address,
		 data: c.methods[f].apply(null, arguments).encodeABI()})
		.once('sending', function(payload){
		    console.log(`.once('sending', function(dumps(${payload})))`);
		})
		.once('sent', function(payload){
		    console.log(`.once('sent', function(dumps(${payload}))`);
		})
		.once('transactionHash', function(hash){
		    console.log(`.once('transactionHash', function(${hash})`);
		})
		.once('receipt', function(receipt){
		    console.log(`.once('receipt', function(${dumps(receipt)})`);
		})
		.on('confirmation', function(confNumber, receipt, latestBlockHash){
		    //console.log(`.on('confirmation', function(${confNumber}, `
		    //+ `${dumps(receipt)}, ${latestBlockHash})`);
		})}}
    for(var m in methods) (methods[m]
			   ? exposeTransactMethod
			   : exposeCallMethod)(contract,m)
    return contract
}
var tok0, tok1, fact, pool, test;

const app = new class App {
    async mintToken(tok, n){
	console.log("MINT TOKEN"+n+"!!");
	tok.more()
	    .on('error', function(error){
		console.log("SEND ERROR", error);
		app.refreshToken(tok, n);
	    })
	    .then(async function(receipt){
		console.log("SEND SUCCESS", receipt);
		app.refreshToken(tok, n);
	    });
    }
    async approveToken(tok, n){
	console.log("APPROVE TOKEN"+n+" FOR EVERYTHING");
	var amt = 1000000000000;
	console.log("APPROVE ", app.PositionMgr, amt);
	tok.approve(app.PositionMgr, amt)
	    .on('error', function(error){
		console.log("SEND ERROR", error);
		app.refreshToken(tok, n);
	    })
	    .then(async function(receipt){
		console.log("SEND SUCCESS", receipt);
		app.refreshToken(tok, n);
	    });
    }
    async refreshUser(){
	var user = app.currentAccount;
	GEBI("user.getBalance").value = web3.eth.getBalance(user);
    }
    async refreshToken(tok, n){
	var user = app.currentAccount;
	GEBI("t"+n+".balanceOf").value = await tok.balanceOf(user);
	GEBI("t"+n+".allowance").value = await tok.allowance(user, app.PositionMgr);
	GEBI("t"+n+".symbol"   ).value = await tok.symbol();
	GEBI("t"+n+".name"     ).value = await tok.name();
    }
    async refreshNFTs(){
	var user = app.currentAccount;
	var ids = await app.getIds(user);
	var arr = [];
	for(var n=0; n < ids.length; ++n){
	    const id = ids[n];
	    console.log("ID", id);
	    var d = await test.order(id);
	    for(var m=0; d[m]!==undefined; ++m)
		/**/     d[m] = undefined;
	    console.log("Order2:", dumps([id,d]));
	    arr.push("<li>");
	    arr.push(`<button onclick='app.cancelPos(${id});return false;'>`);
	    arr.push(                 `app.cancelPos(${id})`);
	    arr.push("</button>");
	    arr.push("<li>");
	    arr.push(dumps([id,d]));
	}
	GEBI("nfts").innerHTML = arr.join("");
    }
    async getIds(user) {
	var ret = [];	
	var ids_length = parseInt(await test.numberOfTokensOfOwner(user));
	for(var n=0; n<ids_length; n++)
	    ret.push(await test.tokenOfOwnerByIndex(user, n));
	return ret;
    }
    async getPriceAtTick(tick){
	var price = await test.getSqrtRatioAtTick(tick);
	price /= (2 ** 96);
	price *= price;
	price = Math.round(price*10000)/10000;
	return price;
    }
    async cancelPos(orderId){
	console.log("CANCEL POS1", orderId);
	test.cancelPos(orderId)
	    .on('error', function(error){
		console.log("SEND ERROR", error);
		app.refreshNFTs();		    
	    })
	    .then(async function(receipt){
		console.log("SEND SUCCESS", receipt);
		app.refreshNFTs();		    
	    });
    }
    async createPos(targetPrice, amt0, amt1){
	var token0 = app.Token0;
	var token1 = app.Token1;
	var fees   = app.fees;
	console.log("CREATE POS0", targetPrice, amt0, amt1);
	console.log("CREATE POS1", token0, token1, fees);
	if(amt0 == 0 && amt1 == 0){
	    throw Exception("both zeros");
	} else if(amt0 == 0 || amt1 == 0){
	    ; // do nothing
	} else {
	    throw Exception("one must be zero");
	}
	console.log("CREATE POS2", token0, token1, fees);
	test.createPos(token0, token1, fees, targetPrice, amt0, amt1)
	    .on('error', function(error){
		console.log("SEND ERROR", error);
		app.refreshNFTs();
	    })
	    .then(async function(receipt){
		console.log("SEND SUCCESS", receipt);
		app.refreshNFTs();
	    });	    
    }
    async start(user){
	app.currentAccount = user;
	web3 = new Web3(ethereum);
	tok0 = expose(new web3.eth.Contract(Token0, app.Token0),
		      {balanceOf:0,symbol:0,name:0,totalSupply:0,allowance:0,
		       approve:1,more:1});
	tok1 = expose(new web3.eth.Contract(Token1, app.Token1),
		      {balanceOf:0,symbol:0,name:0,totalSupply:0,allowance:0,
		       approve:1,more:1});
	pool = expose(new web3.eth.Contract(IUniswapV3Pool, app.Pool),
		      {tickSpacing:0,token0:0,token1:0,fee:0,slot0:0});
	fact = expose(new web3.eth.Contract(UniswapV3Factory, app.factory),
		      {getPool:0,owner:0});
	test = expose(new web3.eth.Contract(PositionMgr, app.PositionMgr),
		      {getPool:0,tokenOfOwnerByIndex:0,order:0,
		       numberOfTokensOfOwner:0,getSqrtRatioAtTick:0,
		       swap:1,
		       cancelPos:1,cancelPos:1});
	var tokenAddress = app.PositionMgr;
	var token0 = app.Token0;
	var token1 = app.Token1;
	var fees = app.fees;
	var poolAddress = app.Pool;
	var tickSpacing = await pool.tickSpacing();
	var slot0 = await pool.slot0();
	var sqrtPriceX96 = slot0.sqrtPriceX96;
	var tick = slot0.tick;
	var price1 = await app.getPriceAtTick( tick);
	var price2 = await app.getPriceAtTick(-tick);
	GEBI("user.address").value = user;
	GEBI("nfts.tokenAddress").value = tokenAddress;
	GEBI('pool.token0').value = token0;
	GEBI('pool.token1').value = token1;
	GEBI('pool.fees').value = fees;
	GEBI('pool.tick').value = tick;
	GEBI('pool.address').value = poolAddress;
	GEBI('pool.tickSpacing').value = tickSpacing;
	GEBI('pool.sqrtPriceX96').value = sqrtPriceX96;
	GEBI('pool.forwardPrice' ).value = price1;
	GEBI('pool.backwardPrice').value = price2;
	app.refreshToken(tok0,0);
	app.refreshToken(tok1,1);
	app.refreshNFTs();
	app.refreshUser();
	setInterval(app.refreshUser, 2000);
    }
    constructor(){
	const app = this;
	Object.assign(app, app_config);
	app.fees = 500;
	app.factory = "0x1F98431c8aD98523631AE4a59f267346ea31F984";
	ethereum.request({ method: 'eth_requestAccounts' })
            .then(function(accounts) {
		if (accounts.length === 0)
		    // MetaMask is locked or the user has not connected any accounts
		    console.log('Please connect to MetaMask.');
		else if (accounts[0] !== app.currentAccount)
		    app.start(accounts[0]);
	    }).catch((err) => {
		if (err.code === 4001)
		    // EIP-1193 userRejectedRequest error
		    // If this happens, the user rejected the connection request.
		    return console.log('Please connect to MetaMask.');
		return console.error(err);
	    });
    }
};
