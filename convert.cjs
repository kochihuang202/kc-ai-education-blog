const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function main() {
    const inputDir = 'C:\\Users\\ji3cp\\Downloads\\New folder (3)';
    const outputDir = 'C:\\Users\\ji3cp\\Documents\\antigravity\\kc-ai-education-blog\\public\\images\\posts\\how-high-can-an-unswayed-person-go';

    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    const files = fs.readdirSync(inputDir).filter(f => f.endsWith('.png'));

    for (const file of files) {
        const match = file.match(/\((\d+)\)/);
        if (match) {
            const num = match[1].padStart(2, '0');
            const outputPath = path.join(outputDir, `graphic-${num}.webp`);
            console.log(`Converting ${file} to graphic-${num}.webp`);
            await sharp(path.join(inputDir, file))
                .webp({ quality: 80 })
                .toFile(outputPath);
        }
    }
    console.log('Conversion complete!');
}

main().catch(console.error);
