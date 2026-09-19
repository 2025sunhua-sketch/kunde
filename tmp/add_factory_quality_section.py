import re

# 读取about.html
with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 构建新的Factory & Quality Assurance区块HTML
new_section = '''
 <!-- Factory & Quality Assurance Section -->
 <section class="factory-quality-section" style="padding: 60px 0; background: #f8f9fa;">
 <div class="container">
 <div class="section-title">
 <h2>Your Trusted Sourcing Partner in China's Power Fittings Hub</h2>
 <p>12+ years curating certified manufacturers, enforcing strict QC, and delivering verified quality to 60+ countries</p>
 </div>

 <div class="factory-gallery" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px;">
 <div class="gallery-item">
 <img src="images/certifications/factory-warehouse-crane.jpg" alt="ISO9001-certified partner warehouse with 5t overhead crane for safe material handling" loading="lazy" decoding="async" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
 <p style="margin-top: 8px; font-size: 14px; color: #555; text-align: center;">Certified Partner Facility</p>
 </div>
 <div class="gallery-item">
 <img src="images/certifications/production-line-heavy-equipment.jpg" alt="Manufacturing partner production line with heavy-duty processing equipment" loading="lazy" decoding="async" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
 <p style="margin-top: 8px; font-size: 14px; color: #555; text-align: center;">Verified Production Line</p>
 </div>
 <div class="gallery-item">
 <img src="images/certifications/automated-production-line.jpg" alt="Automated production line at audited manufacturing partner facility" loading="lazy" decoding="async" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
 <p style="margin-top: 8px; font-size: 14px; color: #555; text-align: center;">Audited Manufacturing Partner</p>
 </div>
 <div class="gallery-item">
 <img src="images/certifications/raw-material-storage.jpg" alt="Organized raw material storage ensuring traceability from source to shipment" loading="lazy" decoding="async" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
 <p style="margin-top: 8px; font-size: 14px; color: #555; text-align: center;">Traceable Supply Chain</p>
 </div>
 </div>

 <div class="factory-gallery" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; max-width: 800px; margin: 0 auto 32px;">
 <div class="gallery-item">
 <img src="images/certifications/brinell-hardness-tester.jpg" alt="In-house Brinell hardness tester for pre-shipment quality verification" loading="lazy" decoding="async" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
 <p style="margin-top: 8px; font-size: 14px; color: #555; text-align: center;">In-House QC Lab</p>
 </div>
 <div class="gallery-item">
 <img src="images/certifications/mechanical-testing-equipment.jpg" alt="Mechanical testing equipment used in independent quality inspection process" loading="lazy" decoding="async" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
 <p style="margin-top: 8px; font-size: 14px; color: #555; text-align: center;">Independent Testing</p>
 </div>
 </div>

 <div class="trust-points" style="background: #fff; padding: 32px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
 <ul style="list-style: none; padding: 0; margin: 0;">
 <li style="margin-bottom: 16px; padding-left: 24px; position: relative; font-size: 15px; line-height: 1.7; color: #333;"><strong style="color: #1a3a5c;">Curated Manufacturing Network:</strong> We partner exclusively with ISO9001:2015 certified factories in Yiwu's power fittings industrial cluster, each audited annually for compliance.</li>
 <li style="margin-bottom: 16px; padding-left: 24px; position: relative; font-size: 15px; line-height: 1.7; color: #333;"><strong style="color: #1a3a5c;">In-House Quality Control:</strong> Every batch undergoes independent testing in our own lab (Brinell hardness, tensile strength, dimensional accuracy) before shipment — we don't rely solely on factory self-inspection.</li>
 <li style="margin-bottom: 16px; padding-left: 24px; position: relative; font-size: 15px; line-height: 1.7; color: #333;"><strong style="color: #1a3a5c;">Full Traceability:</strong> From raw material sourcing to final packaging, every product batch is documented with mill certificates, test reports, and photos for your records.</li>
 <li style="padding-left: 24px; position: relative; font-size: 15px; line-height: 1.7; color: #333;"><strong style="color: #1a3a5c;">Single Point of Accountability:</strong> As your dedicated sourcing partner, KUNDE ELECTRIC takes full responsibility for quality issues — no need to coordinate with multiple factories.</li>
 </ul>
 </div>

 <div style="margin-top: 24px; text-align: center; font-size: 14px; color: #666;">
 <p>Visit our showroom at <strong>A0-033~035, Binwang Market, Yiwu</strong> to inspect samples before ordering.</p>
 </div>
 </div>
 </section>
'''

# 在</section>（advantages-grid之后）和<!-- CTA Section -->之间插入
old_marker = ''' </section>

 <!-- CTA Section -->'''

new_marker = new_section + '''
 <!-- CTA Section -->'''

content = content.replace(old_marker, new_marker)

# 写回文件
with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("about.html修改完成 - 已插入Factory & Quality Assurance区块")
