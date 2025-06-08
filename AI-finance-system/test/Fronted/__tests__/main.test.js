function sumar(a, b) {
  return a + b;
}

function testSumar() {
  const resultado = sumar(2, 3);
  console.assert(resultado === 5, '❌ Test fallido: 2 + 3 debería ser 5');
  console.log('✅ Test pasado: sumar(2, 3) = 5');
}

testSumar();
