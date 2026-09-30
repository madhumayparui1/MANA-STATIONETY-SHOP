import streamlit as st
import os

# 🌟 ১. অনলাইন ক্লাউড লকার (Secrets) থেকে লাইভ ডেটা পড়ার নতুন ফাংশন
def load_live_stock():
    items_list = []
    try:
        # যদি স্ট্রিমলিটের গোপন লকারে 'dokan_stock' থাকে
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
    except Exception as e:
        return []

# ২. কাস্টমারের অনলাইন অর্ডারের তথ্য আলাদা ফাইলে সেভ করার ফাংশন
def save_online_order(c_name, c_phone, c_address, item_name, qty, total):
    file_path = "c:/Users/Dell/Desktop/online_orders.txt"
    try:
        fai = open(file_path, "a", encoding="utf-8")
        fai.write(f"কাস্টমার: {c_name} | ফোন: {c_phone} | ঠিকানা: {c_address} | প্রোডাক্ট: {item_name} | পরিমাণ: {qty} পিস | মোট বিল: {total} Taka\n")
        fai.close()
    except:
        pass


# অনলাইনের ওয়েব পেজ সাজানো (Streamlit Dashboard)
st.set_page_config(page_title="My Smart Stationery Shop", page_icon="🛍️")

st.title("🛍️ WELCOME TO MY SMART STATIONERY SHOP")
st.subheader("কাস্টমার অনলাইন পোর্টাল ও অর্ডার কাউন্টার")
st.write("আমাদের দোকানের লাইভ স্টক নিচে দেওয়া হলো। আপনি এখান থেকেই সরাসরি অর্ডার করতে পারেন:")

# লাইভ ডেটা ক্লাউড লকার থেকে লোড হচ্ছে
live_stock = load_live_stock()

if len(live_stock) == 0:
    st.warning("⚠️ দুঃখিত! এই মুহূর্তে দোকানে কোনো প্রোডাক্ট বা স্টক লোড করা নেই।")
else:
    # --- স্টক দেখানোর টেবিল ছক ---
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown("**📦 প্রোডাক্টের নাম**")
    with col2: st.markdown("**💰 প্রতি পিসের দাম**")
    with col3: st.markdown("**📊 স্টকে আছে**")
    st.write("---")
    
    product_names = []
    for item in live_stock:
        product_names.append(item["name"])
        c1, c2, c3 = st.columns(3)
        with c1: st.write(item["name"])
        with c2: st.write(f"{item['price']} Taka")
        with c3:
            if item["qty"] <= 0: st.error("স্টক আউট!")
            else: st.success(f"{item['qty']} পিস")
    st.write("---")
    
    # --- অনলাইন অর্ডার ফরম ---
    st.subheader("🛒 অনলাইন অর্ডার ফরম (Place Your Order)")
    
    customer_name = st.text_input("আপনার শুভ নাম লিখুন (Your Name):")
    customer_phone = st.text_input("আপনার মোবাইল নম্বর লিখুন (Phone Number):")
    customer_address = st.text_area("আপনার সম্পূর্ণ ডেলিভারি ঠিকানা লিখুন (Full Address):")
    
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
                # অনলাইন রানিং প্র্যাকটিসের জন্য ডিসপ্লে মেসেজ আপডেট
                total_bill = order_qty * item["price"]
                save_online_order(customer_name, customer_phone, customer_address, selected_product, order_qty, total_bill)
                
                st.success(f"🎉 ধন্যবাদ {customer_name}! আপনার অর্ডারটি সফল হয়েছে।")
                st.balloons()
                st.info(f"📦 অর্ডার: {selected_product} ({order_qty} পিস) | মোট বিল: {total_bill} Taka। আমরা খুব জলদি আপনার সাথে যোগাযোগ করছি।")
