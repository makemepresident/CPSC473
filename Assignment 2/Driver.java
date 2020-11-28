import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Scanner;

public class Driver {

    public static void main(String[] args) {

        String filepath = System.getProperty("user.dir") + "\\Datasets" + "\\" + args[0];
        FPGrowth fp = new FPGrowth(filepath, 0.5, 10);
    }
}

class FPGrowth {

    HashMap<Integer, Link> header_table;
    // ArrayList<Link> header_table;
    ArrayList<Link> ordering;
    int db_length;
    double minsup;
    int max_value;

    FPGrowth(String filepath, double minsup, int max_value) {
        this.max_value = max_value;
        this.minsup = minsup;
        gen_header_table(filepath);
        gen_tree(filepath);
    }

    void gen_tree(String filepath) {
        File input = new File(filepath);
        Node root = new Node(0);
        Node pointer = root;
        try {
            Scanner reader = new Scanner(input);
            boolean first = true;
            while(reader.hasNextLine()) {
                if(first) {
                    reader.nextLine();
                    first = false;
                    continue;
                }
                ArrayList<Integer> ordered_elements = reorder(parseElements(reader.nextLine()));
                for(int i : ordered_elements) {
                    if(pointer.children.containsKey(i)) {
                        pointer = pointer.children.get(i);
                        continue;
                    } else {
                        Node t = new Node(i);
                        this.header_table.get(i).pointers.add(t);
                        pointer.children.put(i, t);
                        pointer = t;
                    }
                }
                pointer = root;
            }
            reader.close();
        } catch(FileNotFoundException e) {
            System.out.println(e);
            //TODO: fix
        }
    }

    ArrayList<Integer> reorder(int[] elements) {
        ArrayList<Integer> ordered_elements = new ArrayList<Integer>();
        for(Link l : this.ordering)
            for(int i : elements)
                if(l.value == i)
                    ordered_elements.add(i);
        return ordered_elements;
    }

    void gen_header_table(String filepath) {
        File input = new File(filepath);
        this.header_table = new HashMap<Integer, Link>();
        this.ordering = new ArrayList<Link>();
        try {
            Scanner reader = new Scanner(input);
            boolean first = true;
            while(reader.hasNextLine()) {
                if(first) {
                    this.db_length = Integer.parseInt(reader.nextLine());
                    first = false;
                    continue;
                }
                int[] elements = parseElements(reader.nextLine());
                for(int i : elements) {
                    if(!header_table.containsKey(i)) {
                        header_table.put(i, new Link(i));
                    } else {
                        header_table.get(i).count++;
                    }
                }
            }
            gen_ordering();
            reader.close();
        } catch(FileNotFoundException e) {
            // TODO: ODODODODO
        }
    }

    void gen_ordering() {
        for(Link i : this.header_table.values())
            if(i.count >= this.db_length * this.minsup)
                this.ordering.add(i);
        Collections.sort(this.ordering);
    }

    // void gen_header_table(String filepath) {
    //     File input = new File(filepath);
    //     // ArrayList<Link> unique = new ArrayList<Link>();
    //     Link[] unique = new Link[this.max_value];
    //     try {
    //         Scanner reader = new Scanner(input);
    //         boolean first = true;
    //         while(reader.hasNextLine()) {
    //             if(first) {
    //                 this.db_length = Integer.parseInt(reader.nextLine());
    //                 first = false;
    //                 continue;
    //             }
    //             int[] elements = parseElements(reader.nextLine()); // [2, 3, 5]
    //             for(int i : elements) {
    //                 Link ins = new Link(i);
    //                 if(unique[i] == null) {
    //                     unique[i] = ins;
    //                 } else {
    //                     unique[i].count++;
    //                 }
    //                 // if(!unique.contains(ins)) {
    //                 //     unique.add(new Link(i));
    //                 // } else {
    //                 //     unique.get(i).count++;
    //                 // }
    //             }
    //         }
    //         prune_sort(unique);
    //         reader.close();
    //     } catch(FileNotFoundException e) {
    //         System.out.println(e);
    //         //TODO: handle exception
    //     }
    // }

    int[] parseElements(String line) {
        String elements = line.split("\t")[2];
        int[] arr = Arrays.stream(elements.split(" |\n")).mapToInt(Integer::parseInt).toArray();
        return arr;
    }

    // void prune_sort(Link[] arr) {
    //     this.header_table = new ArrayList<Link>();
    //     for(Link i : arr) {
    //         if(i == null)
    //             continue;
    //         header_table.add(i);
    //     }
    //     Collections.sort(header_table);
    //     for(Iterator<Link> it = header_table.iterator(); it.hasNext();) {
    //         Link i = it.next();
    //         if(i.count < this.db_length * this.minsup)
    //             it.remove();
    //     }
    // }
}

class Node {

    int value;
    int count;
    HashMap<Integer, Node> children;

    Node(int value) {
        this.value = value;
        this.count = 1;
        this.children = new HashMap<Integer, Node>();
    }
}

class Link implements Comparable<Link> {

    int value;
    int count;
    ArrayList<Node> pointers;

    Link(int value) {
        this.value = value;
        this.count = 1;
        this.pointers = new ArrayList<Node>();
    }

    public boolean equals(Object v) {
        if(v instanceof Link) {
            Link cp = (Link) v;
            if(cp.value == this.value)
                return true;
        } else if(v instanceof Integer) {
            int cp = (int) v;
            if(cp == this.value)
                return true;
        }
        return false;
    }

    @Override
    public int hashCode() {
        // TODO Auto-generated method stub
        return super.hashCode();
    }

    @Override
    public int compareTo(Link cp) {
        return cp.count - this.count;
    }
}