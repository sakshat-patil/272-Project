const fs = require('fs');
const path = require('path');

const coverageDir = path.join(__dirname, 'coverage', '.tmp');
const files = fs.readdirSync(coverageDir);

let totalStatements = 0;
let coveredStatements = 0;
let totalFunctions = 0;
let coveredFunctions = 0;
let totalBranches = 0;
let coveredBranches = 0;
let totalLines = 0;
let coveredLines = 0;

files.forEach(file => {
  if (file.endsWith('.json')) {
    const data = JSON.parse(fs.readFileSync(path.join(coverageDir, file), 'utf8'));
    
    Object.values(data).forEach(fileData => {
      // Statements
      const statements = Object.values(fileData.s || {});
      totalStatements += statements.length;
      coveredStatements += statements.filter(s => s > 0).length;
      
      // Functions
      const functions = Object.values(fileData.f || {});
      totalFunctions += functions.length;
      coveredFunctions += functions.filter(f => f > 0).length;
      
      // Branches
      const branches = Object.values(fileData.b || {});
      branches.forEach(branchArray => {
        if (Array.isArray(branchArray)) {
          totalBranches += branchArray.length;
          coveredBranches += branchArray.filter(b => b > 0).length;
        }
      });
      
      // Lines (using statement map)
      if (fileData.statementMap) {
        const lines = Object.keys(fileData.statementMap);
        totalLines += lines.length;
        coveredLines += lines.filter(lineKey => fileData.s[lineKey] > 0).length;
      }
    });
  }
});

const stmtPct = totalStatements > 0 ? ((coveredStatements / totalStatements) * 100).toFixed(2) : 0;
const funcPct = totalFunctions > 0 ? ((coveredFunctions / totalFunctions) * 100).toFixed(2) : 0;
const branchPct = totalBranches > 0 ? ((coveredBranches / totalBranches) * 100).toFixed(2) : 0;
const linePct = totalLines > 0 ? ((coveredLines / totalLines) * 100).toFixed(2) : 0;

console.log('\n================================ Coverage Summary ================================');
console.log(`Statements   : ${stmtPct}% ( ${coveredStatements}/${totalStatements} )`);
console.log(`Branches     : ${branchPct}% ( ${coveredBranches}/${totalBranches} )`);
console.log(`Functions    : ${funcPct}% ( ${coveredFunctions}/${totalFunctions} )`);
console.log(`Lines        : ${linePct}% ( ${coveredLines}/${totalLines} )`);
console.log('==================================================================================\n');
