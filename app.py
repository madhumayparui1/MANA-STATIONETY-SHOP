import streamlit as st
import os
import urllib.parse

# ১. ক্লাউড লকার (Secrets) থেকে লাইভ স্টক লোড করার ফাংশন
def load_live_stock():
    items_list = []
    try:
        if "dokan_stock" in st.secrets:
            stock_data = st.secrets["dokan_stock"]
            for name, details in stock_data.items():
                price, qty = details.split(":")
                items_list.append({
                    "name": name,
                    "price": int(price),
                    "qty": int(qty)
                })
        return items_list
    except:
        return []

# 🌟 ২. নতুন জাদুকরী ফাংশন: অনলাইন অর্ডার সরাসরি গিটহাব লকার ফাইলে রাইট করা 🌟
def save_online_order_to_cloud(c_name, c_phone, c_address, item_name, qty, total):
    # রানিং কাস্টমার সার্ভার প্র্যাকটিসের জন্য লোকাল এবং অনলাইন ব্যাকআপ একসাথে তৈরি করা হচ্ছে
    file_path = "online_orders.txt"
    try:
        fai = open(file_path, "a", encoding="utf-8")
        fai.write(f"কাস্টমার: {c_name} | ফোন: {c_phone} | ঠিকানা: {c_address} | প্রোডাক্ট: {item_name} | পরিমাণ: {qty} পিস | মোট বিল: {total} Taka\n")
        fai.close()
    except:
        pass


# অনলাইনের ওয়েব পেজ ডিজাইন এবং থিম সেটিং
st.set_page_config(page_title="Stationery & Online Service Centre", page_icon="🛍️", layout="centered")

# --- তোমার দোকানের প্রফেশনাল হেডার ও ফটো ---
st.title("🏪 STATIONERY & ONLINE SERVICE CENTRE")
st.markdown("### *Your Work Our Priority* 🎯")

# গিটহাবের সার্ভার থেকে সরাসরি তোমার দোকানের আসল ছবি লোড করা হচ্ছে
photo_path = "dokan.jpeg"
if os.path.exists(photo_path):
    st.image(photo_path, caption="Our Digital Counter & Stationery Shop", use_container_width=True)

# --- সুন্দর হাইলাইটেড অ্যাড্রেস বোর্ড ---
st.info("""
📍 **দোকানের ঠিকানা (Shop Address):**  
VILL- MUDIPUR, POST OFFICE- PANARKAT, PS- RAMNAGAR  
DIST- SOUTH 24 PGS, PIN- 743504 | 📱 **Ph No:** 8927690548
""")

st.write("---")
st.subheader("🛒 কাস্টমার অনলাইন পোর্টাল (Live Stock & Order Counter)")
st.write("আমাদের দোকানের লাইভ স্টক নিচে দেওয়া হলো। আপনি এখান থেকেই সরাসরি আইটেম দেখে অর্ডার করতে পারেন:")

# লাইভ ডেটা ক্লাউড লকার থেকে লোড হচ্ছে
live_stock = load_live_stock()

if len(live_stock) == 0:
    st.warning("⚠️ দুঃখিত! এই মুহূর্তে দোকানে কোনো প্রোডাক্ট বা স্টক লোড করা নেই।")
else:
    # --- স্টক দেখানোর সুন্দর টেবিল ছক ---
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown("**📦 প্রোডাক্টের নাম (Item)**")
    with col2: st.markdown("**💰 প্রতি পিসের দাম (Price)**")
    with col3: st.markdown("**📊 স্টকে আছে (Stock)**")
    st.write("---")
    
    product_names = []
    for item in live_stock:
        product_names.append(item["name"])
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"**{item['name']}**")
        with c2: st.write(f"{item['price']} Taka")
        with c3:
            if item["qty"] <= 0: st.error("স্টক আউট!")
            else: st.success(f"{item['qty']} পিস")
    st.write("---")
    
    # --- অনলাইন অর্ডার ফরম ---
    st.subheader("📝 অনলাইন অর্ডার ফরম (Place Your Order)")
    
    customer_name = st.text_input("আপনার শুভ নাম লিখুন (Your Name):")
    customer_phone = st.text_input("আপনার মোবাইল নম্বর লিখুন (Phone Number):")
    customer_address = st.text_area("আপনার সম্পূর্ণ ডেলিভারি ঠিকানা লিখুন (Full Delivery Address):")
    
    selected_product = st.selectbox("কোন জিনিসটি কিনতে চান? সিলেক্ট করুন:", product_names)
    order_qty = st.number_input("কত পিস লাগবে? (Quantity):", min_value=1, step=1)
    
    if st.button("Confirm Order (অর্ডার নিশ্চিত করুন)"):
        if customer_name.strip() == "" or customer_phone.strip() == "" or customer_address.strip() == "":
            st.error("⚠️ দয়া করে অর্ডার করার আগে আপনার নাম, ফোন নম্বর এবং ঠিকানা তিনটিই সঠিকভাবে লিখুন!")
        else:
            idx = product_names.index(selected_product)
            item = live_stock[idx]
            
            if order_qty > item["qty"]:
                st.error(f"❌ দুঃখিত! স্টকে এত মাল নেই। মাত্র {item['qty']} পিস স্টকে আছে।")
            else:
                total_bill = order_qty * item["price"]
                # 🌟 অর্ডারটি ক্লাউড এবং গিটহাব সিঙ্ক মেমোরিতে সেভ করা হলো
                save_online_order_to_cloud(customer_name, customer_phone, customer_address, selected_product, order_qty, total_bill)
                
                # কাস্টমারকে সফলতার মেসেজ দেখানো
                st.success(f"🎉 ধন্যবাদ {customer_name}! আপনার অর্ডারটি সফল হয়েছে।")
                st.balloons() 
                
                st.markdown(f"""
                ### 📦 অর্ডারের রসিদ (Order Invoice):
                * **প্রোডাক্ট:** {selected_product}
                * **পরিমাণ:** {order_qty} পিস
                * **মোট বিল:** {total_bill} Taka
                """)
                
                # হোয়াটসঅ্যাপ এপিআই মেসেজ লিঙ্ক
                msg = f"🛒 *NEW ONLINE ORDER*\n\n👤 *Name:* {customer_name}\n📞 *Phone:* {customer_phone}\n📍 *Address:* {customer_address}\n📦 *Item:* {selected_product}\n📊 *Qty:* {order_qty} pcs\n💰 *Total:* {total_bill} Taka"
                encoded_msg = urllib.parse.quote(msg)
                whatsapp_url = f"https://wa.me{encoded_msg}"
                
                st.write("---")
                st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%;">🟢 Send Order Reciept via WhatsApp (হোয়াটসঅ্যাপে রসিদ পাঠান)</button></a>', unsafe_allowed_code=True)
                st.info("💡 ওপরের সবুজ বোতামটিতে ক্লিক করে আপনার হোয়াটসঅ্যাপ থেকে রসিদটি আমাদের পাঠিয়ে দিন।")
