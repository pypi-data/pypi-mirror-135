#!/bin/bash -e

export PATH=$PATH:`pwd`/out

export NETWORK=kovan

export PYTHONPATH=`pwd`

unset  WALLET

export WEB3_INFURA_PROJECT_ID=8ad1bacff3ea416989bc1bf33cf96d40
export WEB3_INFURA_SECRET=34ff1cee78be40e4bba76c6e7eb7da2a

export WEB3_PROVIDER_URI=https://kovan.infura.io/v3/$WEB3_INFURA_PROJECT_ID
#export PROVIDER=${WEB3_PROVIDER_URI}

export PUBLIC=0xac83D145634980a3f7bEd4eb5084dd785b195e23
export PRIVATE=0x5e11b147beb73fb3cfc2a2a193484136d2767bc2d4478e41c7e0d1e10d0d4d5e

export WETH9=0xd0A1E359811322d97991E03f863a0C30C2cF029C

echo ">> Using Network $NETWORK..."

exec "$@"
