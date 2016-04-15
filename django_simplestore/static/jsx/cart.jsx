function CartItem(name, qty, unit_cost) {
    //if(qty == undefined && unit_cost == undefined){
   //console.log("N:",name,"CT:",qty,"$:",unit_cost)

    var self = this;
    self.name = name;
    self.event_manager = new ko.subscribable();
    self.subscribe = self.event_manager.subscribe
    self.unit_cost = unit_cost;
    self.shipping_and_handling = 5.0;
    self.qty = ko.observable(qty);
    self.qty.subscribe(function(new_value){
        console.log("GOT:",new_value);
        $.getJSON("/api/v0/cart/update?"+self.name+"="+new_value.toString(),
            function (data){
                ko.postbox.publish("on_cart_data",data);
            //    self.event_manager.notifySubscribers(data,"cart_data");
            }
        );
        console.log("name:",self.name);
    });
    self.total_cost = ko.computed(function(){
        console.log("Unit:",this.unit_cost," * ",this.qty,"=",this.unit_cost*this.qty)
        return (this.unit_cost*this.qty())},this);
}
function CartModel(cart_data){
    var self = this;


    self.items = ko.observableArray([])
    self.discount_code = ko.observable("")

    self.applied_discounts = ko.observableArray([
        ])
    self.has_discounts=ko.computed(function(){
        return self.applied_discounts().length > 0
    });
    self.total_items = ko.computed(function(){
        var count = 0;
        console.log(self.items())
        self.items().forEach(function(item){count+=parseInt(item.qty())});
        return count;
    });
    self.ttl = function(){
        var sum = 0.0;
        self.items().forEach(function(item){sum = sum+item.qty()*item.unit_cost});
        return sum;
    };
    self.total_cost = ko.computed(function(){
        return self.ttl().toFixed(2);
    });
    self.apply_discounts = function(amt,discounts){
        apply_discount=function(discount,amt){
            if(discount["input"].indexOf("rate")>-1){
                return amt - amt * parseFloat(discount["amt"])/100.0
            }else if(discount["input"].indexOf("amount")>-1){
                return amt - parseFloat(discount["amt"])
            }
            return amt;
        };
        if(amt == undefined){ amt = self.ttl() }
        if(discounts == undefined){discounts = self.applied_discounts()}
        $(discounts).each(function(i){amt=apply_discount(discounts[i],amt)})

        return amt;
    };
    self.total_cost_plus = ko.computed(function(){
        return (self.apply_discounts() + self.shipping_and_handling).toFixed(2);
    });
    self.addL=function(L,items,testCondition,parseItem){
        if(testCondition==undefined)testCondition=function(d){return 1;}
        if(parseItem==undefined)parseItem=function(d){return d;}
        items.forEach(function(item){
            if(testCondition(item)){
                L.push(parseItem(item))
            }
        })
    };
    self.updateL=function(L,items,testCondition,parseItem){
        L.removeAll();
        self.addL(L,items,testCondition,parseItem)
        console.log("OK Updated!")
    }
    self.add_items=function(items){
        //items.forEach(function(item){
        //    console.log("Add Item",item);
        //    if(item.product != undefined && item.quantity != undefined){
        //        item = [item.product.product_name,item.quantity,item.product.product_cost]
        //    }
        //    self.items.push(new CartItem(item[0],item[1],item[2]));
        //})
        data_parse = function(item){
            if(item.product != undefined && item.quantity != undefined){
                item =  [item.product.product_name,item.quantity,item.product.product_cost]
            }
            return new CartItem(item[0],item[1],item[2]);
        };

        self.addL(self.items,items,undefined,data_parse)
    };
    self.update_items=function(items){
        self.items.removeAll();
        self.add_items(items)
        console.log("OK ADDED ITEMS:",self.items())
    };
    self.update_discounts=function(discounts){
        self.updateL(self.applied_discounts,discounts)
    };
    self.add_items(cart_data.cart_items);
    self.apply_discount = function(){
        var discount_code = $("#discount_code").val()
        $.getJSON("/api/v0/cart/code/"+discount_code,self.on_cart_data)
    };
    self.on_cart_data=function(data){
        //console.log("Update Cart?");
        //console.log(data);
        self.update_items(data.cart_items)
        self.update_discounts(data.discounts)
    };
    ko.postbox.subscribe("on_cart_data",self.on_cart_data)
    return self
}
function to_currency(a_num){
    console.log(a_num)
    return "$"+a_num.toFixed(2)
}

